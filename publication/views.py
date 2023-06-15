from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PublicationSerializer
from .models import Publication
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
import uuid
from django.utils.html import strip_tags

# Create your views here.
# web
def index(request):
    publications = Publication.objects.order_by('-created_at').filter(is_approved=True)[:3]
    context = {
        'publications': publications
    }

    return render(request,'publication/index.html',context)
    
class IndexView(TemplateView):
    template_name ='publication/index.html'

class PublicationsView(ListView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    template_name = 'publication/publications.html'
    model = Publication
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_approved=True)
        return queryset

class PublicationDetails(DetailView):
    html = '<jats:p>'
    stripped = strip_tags(html)
    
    template_name = 'publication/publication-details.html'
    context_object_name = 'publication'
    queryset = Publication.objects.all()
    
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

