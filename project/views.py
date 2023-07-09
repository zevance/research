from django.shortcuts import render
from .models import Project, UmbrellaProject
from django.views.generic import ListView, DetailView
from .serializer import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def search(request):
    query = request.GET['query']
    results = Project.objects.filter(
		Q(title__icontains=query) | 
		Q(project_type__icontains=query) |
		Q(project_donor__icontains=query)  
	)

    paginator = Paginator(results,10)
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
		'total_results': len(results),
        'projects': paged_results
    }
    return render(request,'core/projects_results.html', context) 

class ProjectsView(ListView):
    template_name = 'core/projects.html'
    model = UmbrellaProject
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_approved=True)
        return queryset

project_list_view =  ProjectsView.as_view()

class UmbrellaProjectDetails(DetailView):
    template_name = 'core/project_details.html'
    context_object_name = 'umbrellaProject'
    queryset   = UmbrellaProject.objects.all()

umbrella_project_details_view = UmbrellaProjectDetails.as_view()

class ProjectDetails(DetailView):
    template_name = 'core/project.html'
    context_object_name = 'project'
    queryset   = Project.objects.all()

project_details_view = ProjectDetails.as_view()

#api view
class ProjectAPIListView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Project.objects.all().filter(is_approved=True)
        data = {}
        if instance:
            data = ProjectSerializer(instance, many = True).data
        return Response(data)
    
project_list_api_view = ProjectAPIListView.as_view()

class ProjectDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(id =pk)
        except Project.DoesNotExist:
            return Response('Project does not exist...!!!!')
        
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pass

project_details_api_view = ProjectDetailsAPIView.as_view()