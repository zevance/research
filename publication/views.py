from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PublicationSerializer
from .models import Publication
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
import uuid
from django.utils.html import strip_tags
from account.models import User
from project.models import Project
from django.http import JsonResponse

# Create your views here.
# web
def index(request):
    html = '<jats:p>'
    stripped = strip_tags(html)
    publications = Publication.objects.order_by('-created_at').filter(is_approved=True)[:2]
    projects = Project.objects.order_by('-created_at').filter(is_approved=True)[:3]
    context = {'publications': publications,'projects': projects}

    return render(request,'core/index.html',context)
    
class IndexView(TemplateView):
    template_name ='publication/index.html'

class PublicationsView(ListView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    template_name = 'core/publications.html'
    model = Publication
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_approved=True)
        return queryset

class PublicationDetails(DetailView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    
    template_name = 'core/publication_details.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()

class ResearchersView(ListView):
    model = User
    template_name = 'core/researchers.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication__isnull=False).distinct()  # Fetch related authors
        return queryset

researchers_list_view = ResearchersView.as_view()

def get_author_publications(request, author_id):
    author = get_object_or_404(User, id=author_id)
    researcher_publications = Publication.objects.filter(author=author)
    context = {'researcher_publications': researcher_publications}
    # Assuming you want to return the publication titles as a JSON response
    #publication_titles = [publication.title for publication in publications]
    return render(request,'core/researcher_publications.html', context)
    
# Api
class PublicationsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Publication.objects.all()
        data = {}
        if instance:
            data = PublicationSerializer(instance, many = True).data
        return Response(data)
    
    # def post(self, request, *args, **kwargs):
    #     publicaction = Publication.objects.create(
    #         title = request.data['title'],
    #     )
    #     serializer = PublicationSerializer(publicaction, many =False)
    #     return Response(serializer.data)
publications_api_view = PublicationsAPIView.as_view()

class PublicationDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Publication.objects.get(id =pk)
        except Publication.DoesNotExist:
            return Response('Publication does not exist...!!!!')
        
    def get(self, request, pk):
        publication = self.get_object(pk)
        serializer = PublicationSerializer(publication, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pass

publications_details_api_view = PublicationDetailsAPIView.as_view()

