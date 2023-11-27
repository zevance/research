from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views import View
import requests
import json
from django.http import JsonResponse
from rest_framework.response import Response
from project.models import Project, UmbrellaProject
from publication.models import Publication
from innovation.models import Innovation
from .choices import license_choices, collection_choices
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import connection
from account.models import Profile
from datetime import datetime
from django.http import HttpResponse
from datetime import datetime
from account.models import User

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

                projects = associated_umbrella_project(request)
                
                choices = {
                    'license-choices': license_choices,
                    'collection_choices': collection_choices,
                   
                }

                return render(request, 'research/publication_detail.html', {
                            'publication': publication,  
                            'license_choices': license_choices,
                            'collection_choices': collection_choices,
                            'projects': projects,
                            })
            else:
                error_message = f"Error retrieving publication data for DOI {doi}."
        else:
            error_message = "DOI not provided."
        return render(request, 'research/add_publication.html', {'error_message': error_message})

add_publication_view = UploadPublicationPageView.as_view()

class AuthorListView(View):
    def get(self,id, *args, **kwargs):
        obj = get_object_or_404(Publication, pk=id)
        co_author = User.objects.order_by('last_name')
        return render(self.request, 'research/co_author.html', {'co_author': co_author,'publication': obj})
        
def author_view(request, id):
    obj = get_object_or_404(Publication, pk=id)
    co_author = User.objects.order_by('last_name')
    return render(request, 'research/co_author.html', {'co_author': co_author,'publication': obj})

# class AddCoAuthorsView(View):
#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             author = request.POST.get('co_authors')
#             author = Publication_Author(author=author)
#             author.save()
#             return redirect('publication_list')

# add_co_author_list_view = AddCoAuthorsView.as_view()

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
        #project_id = request.POST['project_id']
        project_id = request.POST.get('project_id', None)

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
            return render(request, 'research/co_author.html', pk=publication.id)
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


def associated_umbrella_project(request):
    projects = UmbrellaProject.objects.order_by('-created_at').filter(is_approved=True)
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
        projects = associated_umbrella_project(request)
        return render(request, self.template_name, {'projects': projects})

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
        # umbrella_project_id = request.POST['project_id']
        umbrella_project_id = request.POST.get('project_id', None)

        if request.user.is_authenticated:
            user_id = request.user.id
            project = Project(title=title,total_value=total_value,project_status=project_status,project_type=project_type,
            project_pi=project_pi,project_co_pi=project_co_pi,country=country,date_from=date_from,expected_completion_date=expected_completion_date,
            project_member=project_member,project_donor=project_donor,project_partner=project_partner,
            description=description, supporting_document = supporting_document,user_id=user_id
            ,image_path=image_path, umbrella_project_id=umbrella_project_id)
            project.save()
            messages.error(request,'Project added successfuly')
            return redirect('project_list')
        else:
            messages.error(request,'Error while submitting project')
            return render(request, self.template_name)
        
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
        projects = associated_umbrella_project(request)
        return render(request, self.template_name, {'projects': projects})

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        patent = request.POST['patent']
        year_of_innovation = request.POST['year_of_innovation']
        description = request.POST['description']
        project_id = request.POST['project_id']
        image_path = request.FILES['image_path']
        #project_id = request.POST['project_id']
        project_id = request.POST.get('project_id', None)

        if request.user.is_authenticated:
            user_id = request.user.id
            innovation = Innovation(title=title,description=description,patent=patent,
                        year_of_innovation=year_of_innovation,image_path=image_path,user_id=user_id,
                        project_id=project_id)
            innovation.save()
            messages.success(self.request, 'Innovation added successfully')
            return render(request, self.template_name)
        else:
            messages.error(request,'Error while submitting innovation')
            return render(request, self.template_name)

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

#User Profile View
class UserProfileView(View):
    template_name = 'research/profile.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = request.user.id
            has_profile = Profile.objects.filter(user=user_id).exists()
            return render(request, self.template_name, {'has_profile': has_profile})

    def post(self, request, *args, **kwargs):
        user_id = request.POST['user_id']
        specialization = request.POST['specialization']
        research_interests = request.POST['research_interests']
        bio = request.POST['bio']
        image = request.FILES['image']

        if request.user.is_authenticated:
            user_id = request.user.id
            # profile = Profile(specialization=specialization,research_interests=research_interests,
            # bio=bio,image=image, user_id=user_id)
            profile, created = Profile.objects.get_or_create(specialization=specialization,
                    research_interests=research_interests,bio=bio,image=image, user_id=user_id)
            if not created:
                profile.specialization = specialization
                profile.research_interests = research_interests
                profile.bio = bio
                profile.image = image
                profile.use_id = user_id
                profile.save()
                messages.success(self.request, 'User Profile has been added successfully')
                return redirect('profile')
            messages.success(self.request, 'User Profile has been updated successfully')
            return redirect('profile')
        else:
            messages.error(self.request, 'Error while adding User Profile')
            return redirect('profile')

user_profile_view = UserProfileView.as_view()

class GetUserProfile(ListView):
    model =Profile
    template_name = 'research/user_details.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user_id=self.request.user)
        return queryset

user_details_view = GetUserProfile.as_view()

class UpdateUserProfileView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.POST['user_id']
            specialization = request.POST['specialization']
            research_interests = request.POST['research_interests']
            bio = request.POST['bio']
            image = request.FILES['image']

            # Ensure the user exists before updating the profile
            user_profile = Profile.objects.get(user_id=user_id)

            user_profile.specialization = specialization
            user_profile.research_interests = research_interests
            user_profile.bio = bio
            user_profile.image = image
            user_profile.save()

            messages.success(request, 'User Profile updated successfully')
        except Profile.DoesNotExist:
            messages.error(request, 'User Profile not found')
        
        return redirect('profile')

update_user_profile_view = UpdateUserProfileView.as_view()

#End of User Profile View


def staffReport(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (SELECT account_user.id, account_user.title,  concat( first_name, ' ', last_name) AS fullname, account_user.department_code AS department_code, Count( DISTINCT project_project.id) AS projects, Count( DISTINCT publication_publication.id) AS publications, Count(DISTINCT innovation_innovation.id) AS innovations FROM account_user LEFT JOIN project_project  ON project_project.user_id =  account_user.id LEFT JOIN  publication_publication ON publication_publication.author_id = account_user.id LEFT JOIN innovation_innovation ON innovation_innovation.user_id = account_user.id WHERE (publication_publication.is_approved = TRUE OR publication_publication.id IS NULL )  GROUP BY account_user.id) AS temp WHERE publications > 0 OR innovations > 0 OR projects > 0");
        
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

def departmentReportCustom(request):
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    if year is None and quarter is None:
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        date_obj = datetime.strptime(startDate, '%Y-%m-%d')
        startDateString = date_obj.strftime("%d %b %Y")
        date_obj = datetime.strptime(endDate, '%Y-%m-%d')
        endDateString = date_obj.strftime("%d %b %Y")
        description = f"(From {startDateString} to {endDateString})"
    else:
        dates = functions.convertDates(year, quarter)
        startDate = dates['startDate']
        endDate = dates['endDate']
        if quarter == "1":
            ordinal = "First"
        elif quarter == "2":
            ordinal = "Second"
        elif quarter == "3":
            ordinal = "Third"
        else:
            ordinal = "Fourth"
        description = f"({ordinal} Quarter of {year})"
        

    
    report = functions.departmentReport(startDate, endDate)
    

    
    return render(request, 'research/department_report.html', {'data': report, 'description' : description});



def staffReportCustom(request):
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    if year is None and quarter is None:
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        date_obj = datetime.strptime(startDate, '%Y-%m-%d')
        startDateString = date_obj.strftime("%d %b %Y")
        date_obj = datetime.strptime(endDate, '%Y-%m-%d')
        endDateString = date_obj.strftime("%d %b %Y")
        description = f" (From {startDateString} to {endDateString})"
    else:
        dates = functions.convertDates(year, quarter)
        startDate = dates['startDate']
        endDate = dates['endDate']
        if quarter == "1":
            ordinal = "First"
        elif quarter == "2":
            ordinal = "Second"
        elif quarter == "3":
            ordinal = "Third"
        else:
            ordinal = "Fourth"
        description = f"({ordinal} Quarter of {year})"
        

    
    report = functions.staffReport(startDate, endDate)
    

    
    return render(request, 'research/staff_report.html', {'data': report, 'description' : description});


def Charts(request):
    year = request.GET.get('year')
    if(year is None or year == ""):
        description = "All Time"
        year = None
    else:
        description = year
    departmentReport = functions.departmentReport(year);
    print("department report")
    for i in departmentReport:
        print(i)

    facultyReport = functions.facultyReport(year)
    print("faculty report")
    for i in facultyReport:
        print(i)
    


    return render(request, 'research/report_charts.html', {'departmentReport': departmentReport, 'facultyReport': facultyReport, 'description': description, 'year' : year});
    
def downloadExcel(request, year = None):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Research Report.xls"'
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    wp = wb.add_sheet("Publications")
    wp.write(0, 0, 'Faculty', style0)
    wp.write(0, 1, 'Department', style0)
    wp.write(0, 2, 'Author', style0)
    wp.write(0, 3, 'Title', style0)
    wp.write(0, 4, 'Type', style0)
    wp.write(0, 5, 'Publication Year', style0)
    wp.write(0, 6, 'Abstract', style0)

    publications = functions.facultyPublicationReport(year)
    i =1
    for j in publications:
        wp.write(i, 0, j["faculty"])
        wp.write(i, 1, j["department"])
        wp.write(i, 2, j["fullname"])
        wp.write(i, 3, j["publication_title"])
        wp.write(i, 4, j["publication_type"])
        wp.write(i, 5, j["year_of_publication"])
        wp.write(i, 6, j["abstract"])
        i= i + 1
    

    

    wi = wb.add_sheet("Innovations")
    wi.write(0, 0, 'Faculty', style0)
    wi.write(0, 1, 'Departmant', style0)
    wi.write(0, 2, 'Innovator', style0)
    wi.write(0, 3, 'Title', style0)
    wi.write(0, 4, 'Description', style0)
    wi.write(0, 5, 'Year', style0)

    innovations = functions.facultyInnovationReport(year)
    i = 1
    for j in innovations:
        wi.write(i, 0, j["faculty"])
        wi.write(i, 1, j["department"])
        wi.write(i, 2, j["fullname"])
        wi.write(i, 3, j["innovation_title"])
        wi.write(i, 4, j["description"])
        wi.write(i, 5, j["year_of_innovation"])
        i = i + 1



    wpj = wb.add_sheet("Projects")
    wpj.write(0, 0, 'Faculty', style0)
    wpj.write(0, 1, 'Departmant', style0)
    wpj.write(0, 2, 'Principle Investigator', style0)
    wpj.write(0, 3, 'Title', style0)
    wpj.write(0, 4, 'Description', style0)
    wpj.write(0, 5, 'Start Date', style0)
    wpj.write(0, 6, 'End Date', style0)

    i = 1
    projects = functions.facultyProjectReport(year)

    for j in projects:
        wpj.write(i, 0, j["faculty"])
        wpj.write(i, 1, j["department"])
        wpj.write(i, 2, j["fullname"])
        wpj.write(i, 3, j["project_title"])
        wpj.write(i, 4, j["description"])
        wpj.write(i, 5, j["date_from"])
        wpj.write(i, 6, j["expected_completion_date"])
        i = i + 1
    

    

    wb.save(response)
    return response


def test(request):

    data = functions.facultyInnovationReport()
    for i in data:
        print(i)
    return Charts(request)



