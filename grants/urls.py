from django.urls import path
from .views import (
    LandingPageView,
    OpenGrantsView,
    GrantDetailsView,
    GrantApplicationView,
    GrantListView,
    GrantUpdateView,
    DeleteGrantView,
    ApprovedGrantListView,
    DeclinedGrantListView
    )

urlpatterns = [
    path('',LandingPageView.as_view(), name='landing-page'),
    path('open-grant-calls',OpenGrantsView.as_view(), name='open-grant-calls'),
    path('list/', GrantListView.as_view(), name="grant-list"),
    path('approved/', ApprovedGrantListView.as_view(), name="approved-grants"),
    path('declined/', DeclinedGrantListView.as_view(), name="declined-grants"),
    path('update/<uuid:pk>/', GrantUpdateView.as_view(), name="grant-update"),
    path('delete/<uuid:pk>/', DeleteGrantView.as_view(), name="delete-grant"),
    path('grant/application-details/<uuid:pk>', GrantDetailsView.as_view(), name='grant-application-details'),
    path('grant/<uuid:call>/apply',GrantApplicationView.as_view(), name='grant-application'),
]
