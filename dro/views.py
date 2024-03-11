from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from project.models import Project
from publication.models import Publication
from innovation.models import Innovation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import strip_tags
from .forms import CallForApplicationForm
from dro.models import Call
from django.contrib import messages
from event.choices import event_choices
from event.models import Event
from django.urls import reverse_lazy

# Create your views here.
class LandindPageView(LoginRequiredMixin, generic.TemplateView):
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
        projects = Project.objects.filter(response=True, is_approved=True) 
    else:
        projects = None  # Set data to None or handle accordingly

    return render(request, 'dro/approved-projects.html', {'projects': projects})

@login_required
def waiting_approval_project_list_view(request):
    if request.user.is_authenticated and request.user.position == 'Dro':
        projects = Project.objects.filter(response__isnull=True).filter(is_approved=False) 
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

class ApplicationCalls(View):
    template_name ='dro/add-application-call.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        category = request.POST['category']
        document = request.FILES['document']
        
        add_call = Call(name=name, category=category,document=document,user_id=request.user.id) 
        add_call.save()
        messages.success(self.request, 'application submited successfully')
        return redirect('landing')

class AddEventView(View):
    template_name ='dro/add-event.html'

    def get(self, request, *args, **kwargs):
        choices = {
                    'event_choices': event_choices
                }
        return render(request, self.template_name, {"event_choices": event_choices})

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