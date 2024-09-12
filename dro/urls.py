from django.urls import path
from .views import(LandingPageView, 
                    PublicationDetailsView,
                    ProjectDetailView,
                    InnovationDetailsView,
                    AddEventView,
                    EventListView,EventDeleteView,
                    EventUpdateView,ApplicationCallListView,DeleteApplicationCallView)
from . import views 

urlpatterns = [
    path('',LandingPageView.as_view(), name='home'),
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
    # path('application-calls/', ApplicationCalls.as_view(), name='application-calls'),
    path('application-calls/', views.create_application_call, name='application-calls'),
    path('applications/', ApplicationCallListView.as_view(), name='application-list'),
    path('application-update/<uuid:pk>/', views.update_call_view, name='update-call'),
    path('delete-application/<uuid:pk>/', DeleteApplicationCallView.as_view(), name="delete-application"),
    path('add-event/', AddEventView.as_view(), name='add-event'),
    path('events/', EventListView.as_view(), name="events"),
    path('event/<uuid:pk>/',views.event, name='event'),
    path('event/<uuid:pk>/', EventDeleteView.as_view(), name='delete-event'),
    path('event/', EventUpdateView.as_view(), name='update-event'),
    path('excel_report/', views.generate_publication_report, name='generate_publication_report'),
    path('report/', views.department_publications_report, name='report'),
    path('researcher-report/', views.get_all_researchers, name='researcher-report'),
    path('researcher-publication-report', views.get_researcher_publication, name='researcher-publication-report')
]
