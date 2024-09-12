from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import InnovationSerializer
from .models import  Innovation
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.core.paginator import Paginator
import uuid

def search(request):
    query = request.GET['query']
    results = Innovation.objects.filter(
		Q(title__icontains=query) | 
		Q(user__first_name__icontains=query) |
		Q(user__last_name__icontains=query) 
	)

    paginator = Paginator(results,10)
    page = request.GET.get('page')
    paged_results = paginator.get_page(page)

    context = {
		'total_results': len(results),
        'innovations': paged_results
    }
    return render(request,'core/innovations_results.html', context) 


# Create your views here.
# class InnovationsView(ListView):
#     template_name = 'core/innovations.html'
#     model = Innovation
#     paginate_by = 3
#     def get_context_data(self,*args, **kwargs):
#         context = super(InnovationsView, self).get_context_data(*args,**kwargs)
#         context['page_name'] = 'Innovations'
#         return context

def innovation_list_view(request):
    innovations = Innovation.objects.filter(is_approved=True)
    ongoing_innovations = Innovation.objects.filter(is_approved=True, status="In Progress").count()
    completed_innovations = Innovation.objects.filter(is_approved=True, status = "Completed").count()
    total_innovation = innovations.count()

    paginator = Paginator(innovations, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'page_obj': page_obj,
        'ongoing_innovations': ongoing_innovations,
        'completed_innovations': completed_innovations,
        'total_innovation': total_innovation
    }

    return render(request, 'core/innovations.html', context)

class InnovationDetails(DetailView):
    template_name = 'core/innovation_details.html'
    context_object_name = 'innovation'
    queryset = Innovation.objects.all()

#Api view

class InnovationListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Innovation.objects.all().filter(is_approved=True)
        data = {}
        if instance:
            data = InnovationSerializer(instance, many = True).data
        return Response(data)

innovations_api_view = InnovationListAPIView.as_view()

class InnovationDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Innovation.objects.get(id =pk)
        except Innovation.DoesNotExist:
            return Response('Innovation does not exist...!!!!')
        
    def get(self, request, pk):
        innovation = self.get_object(pk)
        serializer = InnovationSerializer(innovation, many=False)
        return Response(serializer.data)
    
innovation_details_api_view = InnovationDetailsAPIView.as_view()