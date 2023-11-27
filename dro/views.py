from django.shortcuts import render
from django.views import generic
from project.models import Project
from publication.models import Publication
from innovation.models import Innovation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import strip_tags

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