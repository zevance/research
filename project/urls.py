from django.urls import path
from .import views

urlpatterns = [
    path('projects/', views.project_list, name='projects'),
    path('projects/search', views.search, name='projects_search'),
    path('project_details/<uuid:pk>/',views.umbrella_project_details_view, name='project_details'),
    path('project/<uuid:pk>/',views.project_details_view, name='project'),
    path('projects/search-project/', views.search_project, name='search'),
    path('api/projects/', views.project_list_api_view),
    path('api/project_details/<uuid:pk>/', views.project_details_api_view),
]
