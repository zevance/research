from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import GrantCreateForm, GrantUpdateForm
from .models import Grant
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class LandingPageView(generic.TemplateView):
    template_name = 'grants/landing_page.html'

def create_grant(request):
    if request.method == 'POST':
        form = GrantCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            #return redirect('success_url')  # Redirect to a success page
            return redirect("grant-application")
    else:
        form = GrantCreateForm(user=request.user)
    return render(request, 'grants/create_grant.html', {'form': form})

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