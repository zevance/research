from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PublicationSerializer, ResearcherSerializer
from .models import Publication
from project.models import Project,UmbrellaProject
from event.models import News, Event
from innovation.models import Innovation
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.db.models import Q
import uuid
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from account.models import User
from rest_framework import generics
from django.utils import timezone

# Create your views here.
# web
def search(request):
    query = request.GET['query']
    results = Publication.objects.filter(
		Q(title__icontains=query) | 
		Q(publisher__icontains=query) |
		Q(author__first_name__icontains=query) |
		Q(author__last_name__icontains=query) |
		Q(publication_type=query)  
	)

    paginator = Paginator(results,10)
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
		'total_results': len(results),
        'publications': paged_results
    }
    return render(request,'core/publications_results.html', context) 

def search_researcher(request):
    query = request.GET['query']
    results = User.objects.filter(
		Q(first_name__icontains=query) |
		Q(last_name__icontains=query)    
	)

    paginator = Paginator(results,10)
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
		'total_results': len(results),
        'researchers': paged_results
    }
    return render(request,'core/researchers_results.html', context) 

def index(request):
    current_year = timezone.now().year
    html = '<jats:p>'
    stripped = strip_tags(html)
    publication_count = Publication.objects.filter(year_of_publication=current_year, is_approved=True)
    count_total_articles = Publication.objects.filter(is_approved=True)
    publications = Publication.objects.order_by('-year_of_publication').filter(author_id__is_alumni=False).filter(is_approved=True)[:3]
    projects = UmbrellaProject.objects.order_by('-created_at').filter(is_approved=True)[:3]
    news = News.objects.order_by('-created_at')[:3]
    events = Event.objects.order_by('-created_at')[:3]
    total_researchers = User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct()
    context = {'publications': publications,'projects': projects,'news': news,'events': events,
            'current_year_publications': publication_count.count(),
            'total_articles': count_total_articles.count(),
            'current_researchers' : total_researchers.count(),}

    return render(request,'core/index.html',context)

class IndexView(ListView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    template_name ='core/index.html'
    model = Publication

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_approved=True)
    #     return queryset

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
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication__isnull=False).filter(publication__is_approved=True).distinct()  # Fetch related authors
        return queryset

researchers_list_view = ResearchersView.as_view()

def get_author_publications(request, author_id):
    author = get_object_or_404(User, id=author_id)
    researcher_publications = Publication.objects.filter(author=author)
    researcher_projects = Project.objects.filter(user=author)
    researcher_innovations = Innovation.objects.filter(user=author)
    context = {'researcher_publications': researcher_publications, 
                'researcher_projects': researcher_projects,
                'researcher_innovations': researcher_innovations}

    return render(request,'core/researcher_publications.html', context)

# Api views
class PublicationsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Publication.objects.all().filter(is_approved=True)
        data = {}
        if instance:
            data = PublicationSerializer(instance, many = True).data
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        serializer = PublicationSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            return Response(serializer.errors)

publications_api_view = PublicationsListAPIView.as_view()

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

publication_details_api_view = PublicationDetailsAPIView.as_view()

class ResearchersListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = User.objects.all().filter(publication__isnull=False).filter(publication__is_approved=True).distinct() 
        data = {}
        if instance:
            data = ResearcherSerializer(instance, many = True).data
        return Response(data)

researcher_api_list_view  = ResearchersListAPIView.as_view()

# def researchers_list_view(request):
#     author_list = User.objects.filter(publication__isnull=False).distinct()
#     # Retrieve all authors who have publications
#     paginator = Paginator(author_list, 6)  # Show 6 authors per page

#     page_number = request.GET.get('page')
#     authors = paginator.get_page(page_number)

#     return render(request, 'researchers/researchers.html', {'authors': authors})