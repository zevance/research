from django.urls import path
from . import views 


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add-publication', views.add_publication_view, name='add-publication'),
    path('upload_publication', views.upload_publication_view, name='upload_publication'),
    path('publication_list', views.publication_list_view, name='publication_list'),
    path('publication/<uuid:pk>', views.publication_details_view, name='publication'),
]
