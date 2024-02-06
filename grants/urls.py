from django.urls import path
from .views import create_grant, LandingPageView,GrantListView,GrantUpdateView

urlpatterns = [
    path('',LandingPageView.as_view(), name='landing-page'),
    path('grant-application/',create_grant, name='grant-application'),
    path('grant-list/', GrantListView.as_view(), name="grant-list"),
    path('grant-update/<uuid:pk>/', GrantUpdateView.as_view(), name="grant-update"),
]
