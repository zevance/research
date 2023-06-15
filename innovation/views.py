from django.shortcuts import render
from .models import  Innovation
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.
class InnovationListView(ListView):
    template_name = 'innovation/innovations.html'
    model = Innovation
    paginate_by = 3

innovation_list_view = InnovationListView.as_view()

class InnovationDetailsView(DetailView):
    template_name = 'innovation/innovation-details.html'
    context_object_name = 'innovation'
    queryset = Innovation.objects.all()

innovation_details_view = InnovationDetailsView.as_view()