from django.urls import path
from . import views
from .views import (
    Collections,
    CollectionDetails,
    IndexView,
    PublicationsView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('publication/', PublicationsView.as_view(), name='publications'),

    path('api/publication/', Collections.as_view(), name='home'),
    path('api/publication/collections/<uuid:pk>', CollectionDetails.as_view(), name='collection_details'),
]
