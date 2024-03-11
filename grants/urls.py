from django.urls import path
from .views import (
    create_grant, 
    LandingPageView,
    GrantListView,
    GrantUpdateView,
    DeleteGrantView,
    ApprovedGrantListView,
    DeclinedGrantListView
    )

urlpatterns = [
    path('',LandingPageView.as_view(), name='landing-page'),
    path('create/',create_grant, name='grant-application'),
    path('list/', GrantListView.as_view(), name="grant-list"),
    path('approved/', ApprovedGrantListView.as_view(), name="approved-grants"),
    path('declined/', DeclinedGrantListView.as_view(), name="declined-grants"),
    path('update/<uuid:pk>/', GrantUpdateView.as_view(), name="grant-update"),
    path('delete/<uuid:pk>/', DeleteGrantView.as_view(), name="delete-grant"),
]
