from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CollectionSerializer, LicenseSerializer, PublicationTypeSerializer
from .models import Collection, Publication, License, PublicationType
from django.views.generic import TemplateView, ListView
from django.views import View
import uuid

# Create your views here.
# web
class IndexView(TemplateView):
    template_name ='publication/index.html'

class PublicationsView(ListView):
    template_name = 'publication/publications.html'
    model = Publication
    paginate_by = 3
    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name) 

class PublicationsDetail(View):
    template_name = 'publication/publication_details.html'
    context_object_name = 'publication'

    def get(self, request,id = None, *args, **kwargs):
        context = {}
        if uuid is None:
            obj = get_object_or_404(Publication, uuid = id)
            context[object] = obj
        return render(request, self.template_name, context) 
    
# Api
class Collections(APIView):
    def get(self, request):
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        collecton = Collection.objects.create(
            name = request.data['name'],
        )
        serializer = CollectionSerializer(collecton, many =False)
        return Response(serializer.data)
    
class CollectionDetails(APIView):
    def get_object(self, pk):
        try:
            return Collection.objects.get(id =pk)
        except Collection.DoesNotExist:
            return Response('Collection does not exist...!!!!')
        
    def get(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pass

class LicenseView(APIView):
    def get(self, request):
        license = License.objects.all()
        serializer = LicenseSerializer(license, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        license = License.objects.create(
            name = request.data['name'],
        )
        serializer = LicenseSerializer(license, many =False)
        return Response(serializer.data)

class PublicationTypeView(APIView):
    def get(self, request):
        publication_type = PublicationType.objects.all()
        serializer = PublicationTypeSerializer(publication_type, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        publication_type = PublicationType.objects.create(
            name = request.data['name'],
        )
        serializer = PublicationTypeSerializer(publication_type, many =False)
        return Response(serializer.data)