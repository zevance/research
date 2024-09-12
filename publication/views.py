import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PublicationSerializer,ResearcherSerializer
from .models import Publication
from project.models import Project, UmbrellaProject
from events.models import News, Event
from innovation.models import Innovation
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.db.models import Q
import uuid
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from account.models import User, Profile
from rest_framework import generics
from django.utils import timezone
from collections import Counter
from django.http import Http404
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

def calculate_average_publications():
    current_year = timezone.now().year
    publications = Publication.objects.filter(is_approved=True)
    publication_years = [pub.year_of_publication for pub in publications]
    year_count = Counter(publication_years)
    total_publications = sum(year_count.values())
    unique_years = len(year_count)
    average_publications = total_publications / unique_years if unique_years else 0
    
    return int(average_publications) 

def index(request):
    current_year = timezone.now().year
    html = '<jats:p>'
    stripped = strip_tags(html)

    average_publications = calculate_average_publications()

    publication_count = Publication.objects.filter(year_of_publication=current_year, is_approved=True)
    count_total_articles = Publication.objects.filter(is_approved=True)
    publications = Publication.objects.order_by('-year_of_publication').filter(author_id__is_alumni=False).filter(is_approved=True)[:3]
    projects = UmbrellaProject.objects.order_by('-created_at').filter(is_approved=True)[:3]
    news = News.objects.order_by('-created_at')[:2]
    events = Event.objects.order_by('-created')[:2]
    total_researchers = User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct()
    year_list = get_year_range()
    context = {
        'publications': publications,
        'average_publications': average_publications,
        'projects': projects,
        'news': news,
        'events': events,
        'current_year_publications': publication_count.count(),
        'total_articles': count_total_articles.count(),
        'current_researchers' : total_researchers.count(),
        'year_list' : year_list
    }

    return render(request,'core/index.html',context)

def get_year_range(start_year=1900, end_year=None):
	year_list = list()
	today = datetime.date.today()
	start_from = start_year
	end_at = end_year or today.year+1
	for year in range(start_from, end_at):
		year_list.append(year)

	year_list.sort(reverse=True)

	return year_list


def publication_list_view(request):
    publications = Publication.objects.filter(is_approved=True)
    total_publications = Publication.objects.filter(is_approved=True).count()
    total_researchers = User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct().count()
    average_publications = calculate_average_publications()

    paginator = Paginator(publications, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'page_obj': page_obj,
        'total_publications': total_publications,
        'total_researchers': total_researchers,
        'average_publications': average_publications
    }

    return render(request, 'core/publications.html', context)

def publication_details_view(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    # author_details = Profile.objects.get(user=publication.author)
    # publications = Publication.objects.get(author=publication.author).exclude(id=pk).order_by('-created_at')[:3]
    try:
        author_details = Profile.objects.get(user=publication.author)
    except Profile.DoesNotExist:
        author_details = None 

    context = {
        'publication': publication,
        'author_details': author_details
    }
    return render(request, 'core/publication_details.html', context)

def search_publications(request):
    faculty = request.GET.get('faculty')
    department = request.GET.get('department')

    publications = Publication.objects.all()
    total_publications = Publication.objects.filter(is_approved=True).count()
    total_researchers = User.objects.filter(publication__isnull=False, publication__is_approved=True).distinct().count()
    average_publications = calculate_average_publications()

    if faculty:
        publications = publications.filter(author__profile__department__faculty__name__iexact=faculty)

    if department:
        publications = publications.filter(author__profile__department__name__iexact=department)

    context = {
        'publications': publications,
        'total_publications': total_publications,
        'total_researchers': total_researchers,
        'average_publications': average_publications
    }

    return render(request, 'core/publication_search_results.html', context)

class ResearchersView(ListView):
    model = User
    template_name = 'core/researchers.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication__isnull=False).filter(publication__is_approved=True).distinct() 
        return queryset

researchers_list_view = ResearchersView.as_view()

def alumini_publications_list_view(request):
    publications = Publication.objects.order_by('-year_of_publication').filter(author_id__is_alumni=True).filter(is_approved=True)[:3]
    projects = Project.objects.order_by('-created_at').filter(user_id__is_alumni=True).filter(is_approved=True)[:3]
    context = {'publications': publications,'projects': projects,}

    return render(request,'core/alumni.html',context)

def get_author_publications(request, author_id):
    author = get_object_or_404(User, id=author_id)
    researcher_publications = Publication.objects.filter(author=author)
    total_researcher_publications = Publication.objects.filter(author=author).count()
    total_researcher_projects = Project.objects.filter(project_pi=author).count()
    total_researcher_innovations = Innovation.objects.filter(user=author).count()
    context = {'researcher_publications': researcher_publications,
            'total_researcher_publications': total_researcher_publications,
            'total_researcher_projects': total_researcher_projects,
            'total_researcher_innovations': total_researcher_innovations
    }

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

publications_details_api_view = PublicationDetailsAPIView.as_view()

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