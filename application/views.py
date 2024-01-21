from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from dro.models import Call
from django.contrib import messages

# Create your views here.
class LandindPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'applications/dashboard.html'

class OpenGrantCallsListView(LoginRequiredMixin, generic.ListView):
    model = Call
    template_name = 'applications/open-research-grants.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category='grant')
        return queryset

class ApplicationCalls(View):
    template_name ='applications/add-application-call.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

