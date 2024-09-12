from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import GrantCreateForm, GrantUpdateForm
from .models import Grant
from dro.models import Call
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class LandingPageView(generic.TemplateView):
    template_name = 'grants/landing_page.html'
        
        
class OpenGrantsView(generic.TemplateView):
    template_name = 'grants/open_grants.html'
    
    def get_open_calls(self):
        open_calls = Call.objects.filter(status="Open")
        return open_calls
    
    def get_context_data(self):
        open_calls = self.get_open_calls()
        context = super().get_context_data()
        context.update({
            "calls": open_calls
        })
        return context
        

class GrantApplicationView(LoginRequiredMixin,  generic.FormView):
    template_name = "grants/apply.html"
    model = Grant
    form_class = GrantCreateForm
    
    def get_call(self):
        call_id = self.kwargs["call"]
        return Call.objects.get(id=call_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        call = self.get_call()
        context.update({"call" : call})
        return context
    
    def get_form_kwargs(self):
        call = self.get_call()
        user = self.request.user
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": user,
            "call": call
        })
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return redirect("open-grant-calls")
        
        
class GrantDetailsView(LoginRequiredMixin,  generic.DetailView):
    template_name = "grants/grant_details.html"
    model = Grant
    

class GrantListView(LoginRequiredMixin, generic.ListView):
    template_name = "grants/grant_list.html"

    def get_queryset(self):
        return Grant.objects.filter(user=self.request.user)

class ApprovedGrantListView(LoginRequiredMixin, generic.ListView):
    template_name = "grants/approved_grants.html"

    def get_queryset(self):
        return Grant.objects.filter(user=self.request.user, is_approved=True)

class DeclinedGrantListView(LoginRequiredMixin, generic.ListView):
    template_name = "grants/declined_grants.html"

    def get_queryset(self):
        return Grant.objects.filter(user=self.request.user, is_approved=False, reason_for_denial__isnull=False)

class GrantUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Grant
    form_class = GrantUpdateForm
    template_name = 'grants/grant_update.html'  # Create this template
    success_url = reverse_lazy('grant-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteGrantView(generic.DeleteView):
    model = Grant
    success_url = reverse_lazy('grant-list')
    
    
    
#
#    def create_grant(request):
#        if request.method == 'POST':
#            form = GrantCreateForm(request.POST, request.FILES, user=request.user)
#            if form.is_valid():
#                form.save()
#                return redirect("grant-application")
#        else:
#            form = GrantCreateForm(user=request.user)
#        return render(request, 'grants/create_grant.html', {'form': form})