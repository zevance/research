from django.urls import path
from . import views
from .views import (
    IndexView,
    PublicationsView,PublicationDetails)

urlpatterns = [
    path('', views.index, name='index'),
    path('publications/', PublicationsView.as_view(), name='publications'),
    path('publication_details/<uuid:pk>/', PublicationDetails.as_view(), name='publication_details'),
    path('researchers/', views.researchers_list_view, name='researchers'),
    path('researcher_publications/<uuid:author_id>/', views.get_author_publications, name='researcher_publications'),

    path('publications/search', views.search, name="publications_search"),
	path('researchers/search', views.search_researcher, name="researchers_search"),

    path('api/publication/', views.publications_api_view, name='home'),
    path('api/publication_details/<uuid:pk>/', views.publication_details_api_view, name='publication_details_api'),
    path('api/researchers/', views.researcher_api_list_view, name='researchers_api_list'),
]
