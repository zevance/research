from django.urls import path
from . import views
from .views import LandindPageView, OpenGrantCallsListView

urlpatterns = [
    path('',LandindPageView.as_view(), name='application-landing'),
    path('open-grant-calls/', OpenGrantCallsListView.as_view(), name='open-grants'),
]