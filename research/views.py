from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView
from django.views import View
import requests
import json
from django.http import JsonResponse
from rest_framework.response import Response
from project.models import Project
from publication.models import Publication
from innovation.models import Innovation
from .choices import license_choices, collection_choices
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name ='research/dashboard.html'

dashboard_view = DashboardPageView.as_view()

class UploadPublicationPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'research/add_publication.html')

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

                return render(request, 'research/publication_detail.html', {
                            'publication': publication,  
                            'license_choices': license_choices,
                            'collection_choices': collection_choices,
                             'projects': projects
                            })
            else:
                error_message = f"Error retrieving publication data for DOI {doi}."
        else:
            error_message = "DOI not provided."
        return render(request, 'research/add_publication.html', {'error_message': error_message})

add_publication_view = UploadPublicationPageView.as_view()


class UploadPublicationView(LoginRequiredMixin, View):
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
                return redirect('add_publication')

            publication = Publication(title=title,abstract=abstract,doi=doi,year_of_publication=year_of_publication,
                        journal_name=journal_name,publisher=publisher,collection=collection,license=license,
                        publication_type=publication_type,author_id=author_id,co_authors=co_authors,
                        number_of_pages=number_of_pages,volume=volume,project_id=project_id)
            publication.save()
            return redirect('publication_list')
        return render(request, 'research/add_publication.html')
    
upload_publication_view = UploadPublicationView.as_view()


class PublicationListView(LoginRequiredMixin, ListView):
    template_name = 'research/all_publications.html'
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


class PublicationDetailsView(LoginRequiredMixin, DetailView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    
    template_name = 'research/publication.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()

publication_details_view = PublicationDetailsView.as_view()


class ApprovedPublicationListView(LoginRequiredMixin, ListView):
    template_name = 'research/approved_publications.html'
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

class DeletePublicationView(LoginRequiredMixin, DeleteView):
    model = Publication
    template_name = 'research/all_publications.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Publication has been deleted successfully')
        return reverse('publication_list')

delete_publication_view = DeletePublicationView.as_view()


class AddProjectView(LoginRequiredMixin, View):
    template_name = 'research/add_project.html'

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
        supporting_document = request.FILES['document']
        image_path = request.FILES['image']

        if request.user.is_authenticated:
            user_id = request.user.id
            project = Project(title=title,total_value=total_value,project_status=project_status,project_type=project_type,
            project_pi=project_pi,project_co_pi=project_co_pi,country=country,date_from=date_from,expected_completion_date=expected_completion_date,
            project_member=project_member,project_donor=project_donor,project_partner=project_partner,
            description=description, supporting_document = supporting_document,user_id=user_id
            ,image_path=image_path)
            project.save()
            messages.error(request,'Project has added successfuly')
            return redirect('project_list')
        else:
            messages.error(request,'Project not added please resubmit')
            return redirect('add_project')
        
add_project_view = AddProjectView.as_view()


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'research/all_projects.html'
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

class ProjectDetailView(LoginRequiredMixin, DetailView):    
    template_name = 'research/research_project.html'
    context_object_name = 'research_project'
    queryset = Project.objects.all()

project_detail_view = ProjectDetailView.as_view()

class ApprovedProjectListView(LoginRequiredMixin, ListView):
    template_name = 'research/approved_projects.html'
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

class ProjectWaitingApprovalListView(LoginRequiredMixin, ListView):
    template_name = 'research/projects_waiting_approval.html'
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

class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'research/all_projects.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Project has been deleted successfully')
        return reverse('project_list')

delete_project_view = DeleteProjectView.as_view()

class UploadInnovationView(LoginRequiredMixin, View):
    template_name = 'research/add_innovation.html'

    def get(self, request, *args, **kwargs):
        projects = associated_project_list(request)
        return render(request, self.template_name, {'projects': projects})

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        patent = request.POST['patent']
        year_of_innovation = request.POST['year_of_innovation']
        description = request.POST['description']
        project_id = request.POST['project_id']
        image_path = request.FILES['image_path']

        if request.user.is_authenticated:
            user_id = request.user.id
            innovation = Innovation(title=title,description=description,patent=patent,
                        year_of_innovation=year_of_innovation,image_path=image_path,user_id=user_id,
                        project_id=project_id)
            innovation.save()
            messages.success(self.request, 'Innovation has been added successfully')
            return redirect('innovation_list')

add_innovation_view = UploadInnovationView.as_view()

class InnovationListView(LoginRequiredMixin, ListView):
    template_name = 'research/all_innovations.html'
    model = Innovation
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user)
        return queryset

innovation_list_view = InnovationListView.as_view()

class DeleteInnovationView(LoginRequiredMixin, DeleteView):
    model = Innovation
    template_name = 'research/all_innovations.html'
  
    def get_success_url(self):
        messages.success(self.request, 'Innovation has been deleted successfully')
        return reverse('innovation_list')

delete_innovation_view = DeleteInnovationView.as_view()

class ApprovedInnovationsListView(LoginRequiredMixin, ListView):
    template_name = 'research/approved_innovations.html'
    model = Innovation
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user).filter(is_approved =True)
        return queryset
        
approved_innovations_list_view = ApprovedInnovationsListView.as_view()

class InnovationsWaitingApprovalListView(LoginRequiredMixin, ListView):
    template_name = 'research/innovations_waiting_approval.html'
    model = Innovation
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user).filter(is_approved =False)
        return queryset
        
waiting_approval_innovations_list_view = InnovationsWaitingApprovalListView.as_view()

class InnovationDetailsView(LoginRequiredMixin, DetailView):    
    template_name = 'research/innovation.html'
    context_object_name = 'innovation'
    queryset = Innovation.objects.all()

innovation_details_view = InnovationDetailsView.as_view()

class ApprovePublicationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']

        Publication.objects.filter(id=id).update(response=True, is_approved=True)
        messages.success(self.request, 'Publication has been approved successfully')
        return redirect('publication_list')

approve_publication_view = ApprovePublicationView.as_view()

class DeclinePublicationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        reason = request.POST['reason']

        Publication.objects.filter(id=id).update(response=False,reason_for_denial=reason)
        messages.success(self.request, 'Publication declined successully')
        return redirect('publication_list')

decline_publication_view = DeclinePublicationView.as_view()