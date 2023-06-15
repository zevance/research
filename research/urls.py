from django.urls import path
from . import views 


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add-publication/', views.add_publication_view, name='add-publication'),
    path('upload_publication/', views.upload_publication_view, name='upload_publication'),
    path('publication_list/', views.publication_list_view, name='publication_list'),
    path('publication/<uuid:pk>/', views.publication_details_view, name='publication'),
    path('approved_publications/', views.approved_publication_list_view, name='approved_publications'),
    path('delete_publication/<uuid:pk>/', views.delete_publication_view, name='delete_publication'),
    path('add_project/', views.add_project_view, name='add_project'),
    path('project_list/', views.project_list_view, name='project_list'),
    path('approved_projects/', views.approved_project_list_view, name='approved_projects'),
    path('projects_waiting_approval/', views.waiting_approval_project_list_view, name='projects_waiting_approval'),
    path('delete_project/<uuid:pk>/', views.delete_project_view, name='delete_project'),
    path('publication_details/', views.associated_project_list),
]
