from django.shortcuts import render
from .models import Project
from django.views.generic import ListView, DetailView
from. serializer import ProjectSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

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

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all().filter(is_approved=True)
    serializer_class= ProjectSerializer

project_list_api_view = ProjectListView.as_view()

class ProjectAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Project.objects.all().filter(is_approved=True)
        data = {}
        if instance:
            data = ProjectSerializer(instance, many = True).data
        return Response(data)
    
    # def post(self, request, *args, **kwargs):
    #     publicaction = Publication.objects.create(
    #         title = request.data['title'],
    #     )
    #     serializer = PublicationSerializer(publicaction, many =False)
    #     return Response(serializer.data)
#project_list_api_view = ProjectAPIView.as_view()