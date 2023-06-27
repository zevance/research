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

    path('api/publication/', views.publications_api_view, name='home'),
    # path('api/collection/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    # path('api/license/', LicenseView.as_view(), name='license'),
    # path('api/license/license/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    # path('api/publication_type/', PublicationTypeView.as_view(), name='publication_type'),
]
