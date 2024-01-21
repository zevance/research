from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from dro.models import Call
from django.contrib import messages

# Create your views here.
class LandindPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'documents/dashboard.html'

class OpenCallsListView(LoginRequiredMixin, generic.ListView):
    model = Call
    template_name = 'documents/open-calls.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category='Grant')
        return queryset