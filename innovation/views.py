from django.shortcuts import render
from .models import  Innovation
from django.views.generic import TemplateView, ListView, DetailView
from .serializer import InnovationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class InnovationListView(ListView):
    template_name = 'core/innovations.html'
    model = Innovation
    paginate_by = 3

innovation_list_view = InnovationListView.as_view()

class InnovationDetailsView(DetailView):
    template_name = 'core/innovation_details.html'
    context_object_name = 'innovation'
    queryset = Innovation.objects.all()

innovation_details_view = InnovationDetailsView.as_view()

# Api Views
class InnovationsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Innovation.objects.all().filter(is_approved=True)
        data = {}
        if instance:
            data = InnovationSerializer(instance, many = True).data
        return Response(data)
    
    # def post(self, request, *args, **kwargs):
    #     publicaction = Publication.objects.create(
    #         title = request.data['title'],
    #     )
    #     serializer = PublicationSerializer(publicaction, many =False)
    #     return Response(serializer.data)
innovation_list_api_view = InnovationsListAPIView.as_view()