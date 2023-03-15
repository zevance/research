from django.shortcuts import render,redirect
from django.views.generic import RedirectView
from django.urls import reverse
from django.views import View
from django.contrib import messages, auth
from django.contrib.auth import login, logout

# Create your views here.
class SignInPageView(View):
    template_name = 'accounts/sign-in.html'
    
    def get(self, request):
        messages = ''
        return render(request, self.template_name, context={'messages': messages})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
            
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Your are now logged in')
            return redirect('projects')
        else:
            messages.error(request, 'Wrong Username or Password')
            return render(request, self.template_name, context={'messages': messages})

sign_in_view = SignInPageView.as_view()

class LogoutView(RedirectView):
    permanent = False
    query_string = True   

    def get_redirect_url(self):
        logout(self.request)
        messages.success(self.request, 'You are now logged out')
        return reverse('sign-in')

logout_view = LogoutView.as_view()
