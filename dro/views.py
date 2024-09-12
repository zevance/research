from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from project.models import Project,UmbrellaProject
from publication.models import Publication
from innovation.models import Innovation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import strip_tags
from .forms import CallForApplicationForm
from dro.models import Call
from django.contrib import messages
from events.models import Event
from django.urls import reverse_lazy
from django.http import HttpResponse
from openpyxl import Workbook
from account.models import Profile, User
from organisation.models import Faculty, Department
from django.db.models import Q
# from event.choices import event_choices

# Create your views here.
class LandingPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dro/dashboard.html'

class PublicationDetailsView(LoginRequiredMixin, generic.DetailView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    
    template_name = 'dro/publication.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()

@login_required
def publication_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        publications = Publication.objects.all  # Retrieve data based on your conditions
    else:
        publications = None  # Set data to None or handle accordingly

    return render(request, 'dro/publication-list.html', {'publications': publications})

@login_required
def approved_publication_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        publications = Publication.objects.filter(response=True,is_approved=True) # Retrieve data based on your conditions
    else:
        publications = None  # Set data to None or handle accordingly

    return render(request, 'dro/approved-publications.html', {'publications': publications})

@login_required
def waiting_approval_publication_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        publications = Publication.objects.filter(response__isnull=True,is_approved=False) # Retrieve data based on your conditions
    else:
        publications = None  # Set data to None or handle accordingly

    return render(request, 'dro/publications-waiting-approval.html', {'publications': publications})

@login_required
def project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.all  # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'dro/project-list.html', {'projects': projects})

@login_required
def approved_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response=True).filter(is_approved=True) # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'dro/approved-projects.html', {'projects': projects})

@login_required
def waiting_approval_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response__isnull=True).filter(is_approved=False) # Retrieve data based on your conditions
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'dro/projects-waiting-approval.html', {'projects': projects})

class ProjectDetailView(LoginRequiredMixin, generic.DetailView):    
    template_name = 'dro/project.html'
    context_object_name = 'research_project'
    queryset = Project.objects.all()

@login_required
def innovation_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.all # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'dro/innovation-list.html', {'innovations': innovations})

class InnovationDetailsView(LoginRequiredMixin, generic.DetailView):    
    template_name = 'dro/innovation.html'
    context_object_name = 'innovation'
    queryset = Innovation.objects.all()

@login_required
def approved_innovation_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.filter(response=True,is_approved=True) # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'dro/approved-innovations.html', {'innovations': innovations})

@login_required
def waiting_approval_innovation_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        innovations = Innovation.objects.filter(response__isnull=True).filter(is_approved=False) # Retrieve data based on your conditions
    else:
        innovations = None  # Set data to None or handle accordingly

    return render(request, 'dro/innovations-waiting-approval.html', {'innovations': innovations})

def create_application_call(request):
    if request.method == 'POST':
        form = CallForApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application_call = form.save(commit=False)
            application_call.user = request.user  
            application_call.save()
            return redirect('application-list')  
    else:
        form = CallForApplicationForm()
    return render(request, 'dro/add-application-call.html', {'form': form})

def update_call_view(request, pk):
    call_instance = get_object_or_404(Call, pk=pk)

    if request.method == 'POST':
        form = CallForApplicationForm(request.POST, request.FILES, instance=call_instance)
        if form.is_valid():
            form.save()
            return redirect('application-list')  
    else:
        form = CallForApplicationForm(instance=call_instance)
    context = {
        'form': form,
        'call': call_instance
    }


    return render(request, 'dro/application-update.html', context)

class ApplicationCallListView(generic.ListView):
    template_name = "dro/application-calls.html"
    context_object_name = 'applications'

    def get_queryset(self):
        return Call.objects.all()

class DeleteApplicationCallView(generic.DeleteView):
    model = Call
    template_name = 'dro/application-list.html'
  
    def get_success_url(self):
        return reverse('application-list')

class AddEventView(View):
    template_name ='dro/add-event.html'

    def get(self, request, *args, **kwargs):
        # choices = {
        #             'event_choices': event_choices
        #         }
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name                   = request.POST['name']
        event_type             = request.POST['event_type']
        venue                  = request.POST['venue']
        date                   = request.POST['date']
        description            = request.POST['description']
        presenter              = request.POST['presenter']
        presenter_position     = request.POST['presenter_position']
        presenter_organisation = request.POST['presenter_organisation']
        meeting_id             = request.POST['meeting_id']
        passcode               = request.POST['passcode']
        link                   = request.POST['link']
        image                  = request.FILES['image']
        
        event = Event(name=name, event_type=event_type,venue=venue,date=date,description=description,
                presenter=presenter,presenter_position=presenter_position,presenter_organisation=presenter_organisation,
                meeting_id=meeting_id,passcode=passcode,link=link,image=image,user_id=request.user.id) 
        event.save()
        messages.success(self.request, 'Event submited successfully')
        return redirect('events')

class EventListView(LoginRequiredMixin,generic.ListView):
    template_name = 'dro/events.html'
    model = Event

def event(request, pk):
    event = get_object_or_404(Event, id=pk)
    choices = {'event_choices': event_choices}
    context = {
        'event' : event,
        'event_choices': event_choices,
    }
    return render(request, 'dro/event-details.html', context)

class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events')

class EventUpdateView(View):
    def post(self, request, *args, **kwargs):
        event_id = request.POST['id']

        # Use get_object_or_404 to retrieve the object
        event = get_object_or_404(Event, id=event_id)

        # Update the fields
        event.name = request.POST['name']
        event.event_type = request.POST['event_type']
        event.venue = request.POST['venue']
        event.date = request.POST['date']
        event.description = request.POST['description']
        event.presenter = request.POST['presenter']
        event.presenter_position = request.POST['presenter_position']
        event.presenter_organisation = request.POST['presenter_organisation']
        event.meeting_id = request.POST['meeting_id']
        event.passcode = request.POST['passcode']
        event.link = request.POST['link']

        # Save the updated object
        event.save()

        messages.success(request, 'Event updated successfully')
        return redirect('events')

def department_publications_report(request):
    # Create a dictionary to hold department names and their publication counts
    departments_data = []

    # Query all faculties and iterate over departments
    faculties = Faculty.objects.all()

    for faculty in faculties:
        departments = faculty.department.all()  # Get all departments under the faculty

        for department in departments:
            # Count the number of publications for each department
            num_publications = Publication.objects.filter(author__profile__department=department).count()
            num_projects = UmbrellaProject.objects.filter(user__profile__department=department).count()
            # Add the department name and publication count to the list
            departments_data.append({
                'department_name': department.name,
                'num_publications': num_publications,
                'num_projects': num_projects
            })

    # Pass the departments' data to the template
    context = {
        'departments_data': departments_data
    }

    return render(request, 'dro/report.html', context)

def generate_publication_report(request):
    # Create a new Excel workbook and worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Publications Report"

    # Add headers to the Excel sheet
    headers = ["Fullname", "Faculty", "Department", "Number of Publications"]
    ws.append(headers)

    # Query for faculties and iterate over them
    faculties = Faculty.objects.all()

    for faculty in faculties:
        departments = faculty.department.all()  # Get all departments under the faculty

        for department in departments:
            profiles = department.user.all()  # Get all users in the department

            for profile in profiles:
                user = profile.user
                # Filter publications for the user
                num_publications = Publication.objects.filter(author=user).count()

                # Only include users with at least 1 publication
                if num_publications > 0:
                    # Append a row with the faculty, department, user, and number of publications
                    fullname = f"{user.title} {user.first_name} {user.last_name}"
                    ws.append([fullname, faculty.name, department.name, num_publications])

    # Set up the HTTP response with the appropriate Excel headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="publications_report.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

@login_required
def get_all_researchers(request):
    researchers =User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct()
    context = {
        'researchers': researchers
    }
    return render(request, 'dro/staff.html', context)

@login_required
def get_researcher_publication(request):
    researcher = request.GET.get('researcher')
    publications = Publication.objects.filter(author=researcher).order_by('-year_of_publication')
    researchers =User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct()
    context = {
        'publications': publications,
        'researchers': researchers
    }
    return render(request,'dro/staff.html', context) 