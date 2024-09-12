from django.shortcuts import render
from .models import Project, UmbrellaProject
from django.views.generic import ListView, DetailView
from .serializer import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
    query = request.GET['query']
    results = UmbrellaProject.objects.filter(
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

# Create your views here.
class ProjectsView(ListView):
    template_name = 'core/projects.html'
    model = UmbrellaProject
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_approved=True)
        return queryset

project_list_view =  ProjectsView.as_view()

def project_list(request):
    umbrella_projects = UmbrellaProject.objects.order_by('-created_at').filter(is_approved=True)
    projects = Project.objects.order_by('-created_at').filter(is_approved=True)[:5]
    grant_based_projects = Project.objects.filter(is_approved=True, project_type="Grant based").count()
    consultancy_based_projects = Project.objects.filter(is_approved=True, project_type="Consultancy").count()
    ongoing_projects = UmbrellaProject.objects.filter(is_approved=True, project_status="On Going").count()
    completed_projects = UmbrellaProject.objects.filter(is_approved=True, project_status="Completed").count()
    total_umbrella_projects =  ongoing_projects + completed_projects

    paginator = Paginator(umbrella_projects, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'umbrella_projects': page_obj, 
              'projects': projects,
              'grant_based_projects': grant_based_projects,
              'consultancy_based_projects': consultancy_based_projects,
              'ongoing_projects': ongoing_projects,
              'completed_projects': completed_projects,
              'total_umbrella_projects': total_umbrella_projects
            }
    return render(request, 'core/projects.html', context)

def search_project(request):
    umbrella_projects = UmbrellaProject.objects.order_by('-created_at').filter(is_approved=True)[:4]
   
    queryset_list = Project.objects.order_by('-created_at')

    filters = Q()

    if 'project_type' in request.GET:
        project_type = request.GET['project_type']

    if project_type:
        filters |= Q(project_type__icontains=project_type)

    if 'project_status' in request.GET:
        project_status = request.GET['project_status']

    if project_status:
        filters |= Q(project_status__icontains=project_status)

    queryset_list = queryset_list.filter(filters)

    context = {
      'projects' : queryset_list,
      'total_results' : queryset_list.count(),
      'umbrella_projects': umbrella_projects ,
      'values' : request.GET
    }
    return render(request,'core/search_project.html', context) 

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