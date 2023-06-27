from django.shortcuts import render
from .models import Project
from django.views.generic import ListView, DetailView

# Create your views here.
class ProjectsView(ListView):
    template_name = 'core/projects.html'
    model = Project
    paginate_by = 3


project_list_view = ProjectsView.as_view()

class ProjectDetails(DetailView):
    template_name = 'core/project_details.html'
    context_object_name = 'project'
    queryset   = Project.objects.all()

project_details_view = ProjectDetails.as_view()