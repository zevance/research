from django.urls import path
from . import views 

urlpatterns = [
    path('sign-in', views.sign_in_view, name='sign-in'),
    path('sign-out', views.logout_view, name='sigtn-out'),
]
