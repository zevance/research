from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CollectionSerializer
from .models import Collection
from django.views.generic import TemplateView
from django.views import View

# Create your views here.
class IndexView(TemplateView):
    template_name ='publication/index.html'

class PublicationsView(View):
    template_name = 'publication/publications.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name) 
    
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