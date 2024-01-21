from django.urls import path
from . import views
from .views import LandindPageView, OpenCallsListView

urlpatterns = [
    path('',LandindPageView.as_view(), name='landing-page'),
    path('open-calls', OpenCallsListView.as_view(), name='open-calls'),
]