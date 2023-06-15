from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views import View
import requests
import json
from django.http import JsonResponse
from rest_framework.response import Response
from project.models import Project
from publication.models import Publication
from .choices import license_choices, collection_choices
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
class DashboardPageView(TemplateView):
    template_name ='research/dashboard.html'

dashboard_view = DashboardPageView.as_view()

class UploadPublicationPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'research/add-publication.html')

    def post(self, request, *args, **kwargs):
        doi = request.POST.get('doi')
        if doi:
            url = f'https://api.crossref.org/works/{doi}'
           
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                publication = {
                    'type': data['message']['type'],
                    'title': data['message']['title'][0],
                    'author_1': data['message']['author'][0]['given'] + ' ' + data['message']['author'][0]['family'],
                    'co_authors': [author['given'] + ' ' + author['family'] for author in data['message']['author'][1:]],
                    'journal': data['message']['container-title'][0],
                    #'abstract': data['message']['abstract'],
                    'year': data['message']['issued']['date-parts'][0][0],
                    'volume': data['message']['volume'],
                    #'issue': data['message']['issue'],
                    'pages': data['message']['page'],
                    'publisher': data['message']['publisher'],
                    'doi': data['message']['DOI'],
                    #'country': data['message']['country'],
                }

                projects = associated_project_list(request)

                choices = {
                    'license-choices': license_choices,
                    'collection_choices': collection_choices,
                   
                }

                return render(request, 'research/publication-detail.html', {
                            'publication': publication,  
                            'license_choices': license_choices,
                            'collection_choices': collection_choices,
                             'projects': projects
                            })
            else:
                error_message = f"Error retrieving publication data for DOI {doi}."
        else:
            error_message = "DOI not provided."
        return render(request, 'research/add-publication.html', {'error_message': error_message})

add_publication_view = UploadPublicationPageView.as_view()


class UploadPublicationView(View):
    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        abstract = request.POST['abstract']
        doi = request.POST['doi']
        year_of_publication = request.POST['year_of_publication']
        journal_name = request.POST['journal_name']
        publisher = request.POST['publisher']
        collection = request.POST['collection']
        license = request.POST['license']
        publication_type = request.POST['publication_type']
        author_id = request.POST['author_id']
        co_authors = request.POST['co_authors']
        number_of_pages = request.POST['pages']
        volume = request.POST['volume']
        project_id = request.POST['project_id']

        if request.user.is_authenticated:
            author_id = request.user.id
            if Publication.objects.filter(doi=doi).exists():
                messages.error(request,'Publication with the provided DOi is already available')
                return redirect('add-publication')

            publication = Publication(title=title,abstract=abstract,doi=doi,year_of_publication=year_of_publication,
                        journal_name=journal_name,publisher=publisher,collection=collection,license=license,
                        publication_type=publication_type,author_id=author_id,co_authors=co_authors,
                        number_of_pages=number_of_pages,volume=volume,project_id=project_id)
            publication.save()
            return render(request, 'research/all-publications.html')
        return render(request, 'research/add-publication.html')
    
upload_publication_view = UploadPublicationView.as_view()


class PublicationListView(ListView):
    template_name = 'research/all-publications.html'
    model = Publication
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(author_id=self.request.user)
        return queryset
        
publication_list_view = PublicationListView.as_view()


class PublicationDetailsView(DetailView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    
    template_name = 'research/publication.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()

publication_details_view = PublicationDetailsView.as_view()


class ApprovedPublicationListView(ListView):
    template_name = 'research/approved-publications.html'
    model = Publication
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(author_id=self.request.user).filter(is_approved =True)
        return queryset
        
approved_publication_list_view = ApprovedPublicationListView.as_view()


def associated_project_list(request):
    projects = Project.objects.order_by('-created_at').filter(is_approved=True)
    return projects

class DeletePublicationView(DeleteView):
    model = Publication
    template_name = 'research/all-publications.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Publication has been deleted successfully')
        return reverse('publication_list')

delete_publication_view = DeletePublicationView.as_view()


class AddProjectView(View):
    template_name = 'research/add-project.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_id = request.POST['user_id']
        title = request.POST['title']
        total_value = request.POST['total_value']
        project_status = request.POST['project_status']
        project_type = request.POST['project_type']
        date_from = request.POST['date_from']
        expected_completion_date = request.POST['expected_completion_date']
        project_pi = request.POST['project_pi']
        project_co_pi = request.POST['project_co_pi']
        country = request.POST['country']
        description = request.POST['description']
        project_member = request.POST.get('c_data')
        project_partner = request.POST.get('concatenated_data')
        project_donor = request.POST.get('concat_data')
        supporting_document = request.FILES['supporting_document']

        fs = FileSystemStorage()
        name = fs.save(supporting_document.name, supporting_document)

        if request.user.is_authenticated:
            user_id = request.user.id
            project = Project(title=title,total_value=total_value,project_status=project_status,project_type=project_type,
            project_pi=project_pi,project_co_pi=project_co_pi,country=country,date_from=date_from,expected_completion_date=expected_completion_date,
            project_member=project_member,project_donor=project_donor,project_partner=project_partner,
            description=description,supporting_document= fs.url(name),user_id=user_id)
            project.save()
            return render(request, self.template_name)
        else:
            pass
        
add_project_view = AddProjectView.as_view()


class ProjectListView(ListView):
    template_name = 'research/all-projects.html'
    model = Project
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user)
        return queryset

project_list_view = ProjectListView.as_view()


class ApprovedProjectListView(ListView):
    template_name = 'research/approved-projects.html'
    model = Project
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user).filter(is_approved =True)
        return queryset
        
approved_project_list_view = ApprovedProjectListView.as_view()

class ProjectWaitingApprovalListView(ListView):
    template_name = 'research/projects-waiting-approval.html'
    model = Project
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user).filter(is_approved =False)
        return queryset
        
waiting_approval_project_list_view = ProjectWaitingApprovalListView.as_view()

class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'research/all-projects.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Project has been deleted successfully')
        return reverse('project_list')

delete_project_view = DeleteProjectView.as_view()