from django.urls import path
from . import views 


urlpatterns = [
    #PUBLICATIONS FUNCTIONS
    path('', views.dashboard_view, name='dashboard'),
    path('add_publication/', views.add_publication_view, name='add_publication'),
    path('upload_publication/', views.upload_publication_view, name='upload_publication'),
    path('publication_list/', views.publication_list_view, name='publication_list'),
    path('publication/<uuid:pk>/', views.publication_details_view, name='publication'),
    path('approved_publications/', views.approved_publication_list_view, name='approved_publications'),
    path('delete_publication/<uuid:pk>/', views.delete_publication_view, name='delete_publication'),
    path('publication_details/', views.associated_project_list),
    #END OF PUBLICATIONS FUNCTIONS

    #DRO FUNCTIONS
    path('approve_publication/<uuid:pk>/', views.approve_publication_view, name='approve_publication'),
    path('decline_publication/<uuid:pk>', views.decline_publication_view, name='decline_publication'),
    path('dro_publications/', views.dro_publication_list_view, name='dro_publications'),
    path('approved_dro_publications/', views.approved_dro_publication_list_view, name='approved_dro_publications'),
    path('dro_projects/', views.dro_project_list_view, name='dro_projects'),
    path('approved_dro_projects/', views.approved_dro_project_list_view, name='approved_dro_projects'),
    path('waiting_dro_approval/', views.waiting_dro_approval_project_list_view, name='waiting_dro_approval'),
    path('approve_project/<uuid:pk>/', views.approve_project_view, name='approve_project'),
    path('decline_project/<uuid:pk>', views.decline_project_view, name='decline_project'),
    path('dro_innovations/', views.dro_innovation_list_view, name='dro_innovations'),
    path('approved_dro_innovations/', views.approved_dro_innovation_list_view, name='approved_dro_innovations'),
    path('innovations_waiting_dro_approval/', views.waiting_dro_approval_project_list_view, name='innovations_waiting_dro_approval'),
    path('approve_innovation/<uuid:pk>/', views.approve_innovation_view, name='approve_innovation'),
    path('decline_innovation/<uuid:pk>', views.decline_innovation_view, name='decline_innovation'),
    #END OF DRO FUNCTIONS

    #RESEARCH PROJECT FUNCTIONS
    path('add_project/', views.add_project_view, name='add_project'),
    path('project_list/', views.project_list_view, name='project_list'),
    path('research_project/<uuid:pk>/', views.project_detail_view, name='research_project'),
    path('approved_projects/', views.approved_project_list_view, name='approved_projects'),
    path('projects_waiting_approval/', views.waiting_approval_project_list_view, name='projects_waiting_approval'),
    path('delete_project/<uuid:pk>/', views.delete_project_view, name='delete_project'),
    # END OF RESEARCH PROJECT FUNCTIONS

    #INNOVATIONS FUNCTIONS
    path('upload_innovation/', views.add_innovation_view, name='upload_innovation'),
    path('innovation_list/', views.innovation_list_view, name='innovation_list'),
    path('delete_innovation/<uuid:pk>/', views.delete_project_view, name='delete_innovation'),
    path('approved_innovations/', views.approved_innovations_list_view, name='approved_innovations'),
    path('innovations_waiting_approval/', views.waiting_approval_innovations_list_view, name='innovations_waiting_approval'),
    path('innovation/<uuid:pk>/', views.innovation_details_view, name='innovation'),
    #END OFINNOVATIONS FUNCTIONS

    #REPORT FUNCTIONS
    path('staff_report/', views.staffReport),
    path('department_report/', views.departmentReport),
    #END OF REPORT FUNCTIONS
]
