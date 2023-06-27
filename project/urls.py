from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list_view, name='projects'),
    path('project_details/<uuid:pk>/',views.project_details_view, name='project_details'),
]