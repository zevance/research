from django.shortcuts import render
from .models import Project
from django.views.generic import ListView, DetailView

# Create your views here.
class ProjectsView(ListView):
    template_name = 'project/projects.html'
    model = Project
    paginate_by = 3

class ProjectDetails(DetailView):
    template_name = 'project/project-details.html'
    context_object_name = 'project'
    queryset = Project.objects.all()