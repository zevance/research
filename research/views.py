from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
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
from django.db import connection


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

#DRO FUNCTIONS
#Publication DRO Functions
#publications that needs approval by dro
class ApprovePublicationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']

        Publication.objects.filter(id=id).update(response=True, is_approved=True)
        messages.success(self.request, 'Publication has been approved successfully')
        return redirect('dro_publications')

approve_publication_view = ApprovePublicationView.as_view()

class DeclinePublicationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        reason = request.POST['reason']

        Publication.objects.filter(id=id).update(response=False,reason_for_denial=reason)
        messages.success(self.request, 'Publication declined successully')
        return redirect('dro_publications')

decline_publication_view = DeclinePublicationView.as_view()

def dro_publication_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        publications = Publication.objects.filter(response__isnull=True)  # Retrieve data based on your conditions
    else:
        publications = None  # Set data to None or handle accordingly

    return render(request, 'research/all_publications.html', {'publications': publications})

#approved publications by dro
def approved_dro_publication_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        publications = Publication.objects.filter(response=True).filter(is_approved=True) # Retrieve data based on your conditions
    else:
        publications = None  # Set data to None or handle accordingly

    return render(request, 'research/approved_dro_publications.html', {'publications': publications})

#Project DRO Functions
#projects that needs dro approval
def dro_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response__isnull=True)  # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'research/dro_projects_list.html', {'projects': projects})

#approved projects by dro
def approved_dro_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response=True).filter(is_approved=True) # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'research/approved_dro_projects.html', {'projects': projects})

#waiting dro approval projects 
def waiting_dro_approval_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response__isnull=True).filter(is_approved=False) # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'research/waiting_dro_approval.html', {'projects': projects})

class ApproveProjectView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']

        Project.objects.filter(id=id).update(response=True, is_approved=True)
        messages.success(self.request, 'Project has been approved successfully')
        return redirect('dro_projects')

approve_project_view = ApproveProjectView.as_view()

class DeclineProjectView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        reason = request.POST['reason']

        Project.objects.filter(id=id).update(response=False,reason_for_denial=reason)
        messages.success(self.request, 'Project declined successully')
        return redirect('dro_projects')

decline_project_view = DeclineProjectView.as_view()

#Innovation DRO Functions
#innovations that needs dro approval 
def dro_innovation_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.filter(response__isnull=True)  # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'research/dro_innovation_list.html', {'innovations': innovations})

#approved innovations by dro
def approved_dro_innovation_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.filter(response=True).filter(is_approved=True) # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'research/approved_dro_innovations.html', {'innovations': innovations})

#innovations waiting dro approval 
def waiting_dro_approval_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.filter(response__isnull=True).filter(is_approved=False) # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'research/innovations_waiting_dro_approval.html', {'innovations': innovations})

class ApproveInnovationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']

        Innovation.objects.filter(id=id).update(response=True, is_approved=True)
        messages.success(self.request, 'Innovation has been approved successfully')
        return redirect('dro_projects')

approve_innovation_view = ApproveInnovationView.as_view()

class DeclineInnovationView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST['id']
        reason = request.POST['reason']

        Innovation.objects.filter(id=id).update(response=False,reason_for_denial=reason)
        messages.success(self.request, 'Innovation declined successully')
        return redirect('dro_projects')

decline_innovation_view = DeclineInnovationView.as_view()
    
#END OF DRO FUNCTIONS

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

def staffReport(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (SELECT account_user.id, account_user.title,  concat( first_name, ' ', last_name) AS fullname, account_user.department_code AS department_code, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM account_user LEFT JOIN project_project  ON project_project.user_id =  account_user.id LEFT JOIN  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN innovation_innovation ON innovation_innovation.user_id = account_user.id  GROUP BY account_user.id) AS temp WHERE publications > 0 OR innovations > 0 OR projects > 0");
        
        columns = [col[0] for col in cursor.description]
        report = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # report = User.objects.select_related('user')
    for i in report:
        print(i)

    return render(request, 'research/staff_report.html', {'data': report});

def departmentReport(request):
	 
    with connection.cursor() as cursor:
        cursor.execute("SELECT account_user.department_code AS department, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM account_user LEFT JOIN project_project  ON project_project.user_id =  account_user.id LEFT JOIN  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL ) AND account_user.department_code IS NOT NULL GROUP BY account_user.department_code ");
        
        columns = [col[0] for col in cursor.description]
        report = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # report = User.objects.select_related('user')
    for i in report:
        print(i)

    return render(request, 'research/department_report.html', {'data': report});