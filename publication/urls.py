from django.urls import path
from . import views
# from .views import PublicationsView

urlpatterns = [
    path('', views.index, name='index'),
	path('publications/search', views.search, name="publications_search"),
	path('researchers/search', views.search_researcher, name="researchers_search"),
    # path('publications/', PublicationsView.as_view(), name='publications'),
    path('publications/', views.publication_list_view, name='publications'),
    # path('publication_details/<uuid:pk>/', PublicationDetails.as_view(), name='publication_details'),
    path('publication_details/<uuid:pk>/', views.publication_details_view, name='publication_details'),
    path('search_publications/', views.search_publications, name='search_publications'),
    path('researchers/', views.researchers_list_view, name='researchers'),
    path('researcher_publications/<uuid:author_id>/', views.get_author_publications, name='researcher_publications'),
    path('alumni/', views.alumini_publications_list_view, name='alumni'),
   
    path('api/publication/', views.publications_api_view, name='home'),
    path('api/publication_details/<uuid:pk>/', views.publications_details_api_view, name='publication_details_api'),
    path('api/researchers/', views.researcher_api_list_view, name='researchers_api_list'),
    # path('api/collection/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    # path('api/license/', LicenseView.as_view(), name='license'),
    # path('api/license/license/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    # path('api/publication_type/', PublicationTypeView.as_view(), name='publication_type'),
]
