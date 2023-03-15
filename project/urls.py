from django.urls import path
from .views import ProjectsView, ProjectDetails

urlpatterns = [
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('project-details/<uuid:pk>',ProjectDetails.as_view(), name='project-details'),
]
