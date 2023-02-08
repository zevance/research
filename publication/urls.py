from django.urls import path
from . import views
from .views import (
    Collections,CollectionDetails,IndexView,
    PublicationsView,PublicationDetails, LicenseView, PublicationTypeView, InnovationsView, InnovationDetails)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('publication/', PublicationsView.as_view(), name='publications'),
    path('publication-details/<uuid:pk>', PublicationDetails.as_view(), name='publication-details'),
    path('innovation/', InnovationsView.as_view(), name='innovations'),
    path('innovation-details/<uuid:pk>', InnovationDetails.as_view(), name='innovation-details'),

    path('api/collection/', Collections.as_view(), name='home'),
    path('api/collection/collections/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    path('api/license/', LicenseView.as_view(), name='license'),
    #path('api/license/license/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
    path('api/publication_type/', PublicationTypeView.as_view(), name='publication_type'),
]
