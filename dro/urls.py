from django.urls import path
from .views import LandindPageView, PublicationDetailsView,ProjectDetailView,InnovationDetailsView
from . import views

urlpatterns = [
    path('',LandindPageView.as_view(), name='home'),
    path('publication/<uuid:pk>/', PublicationDetailsView.as_view(), name='publication-details'),
    path('publications/', views.publication_list_view, name='publication-list'),
    path('approved-publications/', views.approved_publication_list_view, name='approved-publications'),
    path('publications-waiting-approval/', views.waiting_approval_publication_list_view, name='publications-waiting-approval'),
    path('projects/', views.project_list_view, name='project-list'),
    path('project/<uuid:pk>/',ProjectDetailView.as_view(), name='project-details'),
    path('approved-projects/', views.approved_project_list_view, name='approved-projects'),
    path('projects-waiting-approval/', views.waiting_approval_project_list_view, name='projects-waiting-approval'),
    path('innovations/', views.innovation_list_view, name='innovation-list'),
    path('innovation/<uuid:pk>/', InnovationDetailsView.as_view(), name='innovation-details'),
    path('approved-innovations/', views.approved_innovation_list_view, name='approved-innovations'),
    path('innovations-waiting-approval/', views.waiting_approval_innovation_list_view, name='innovations-waiting-approval'),
]
