from django.urls import path
from . import views 


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('add-publication', views.add_publication_view, name='add-publication'),
    #path('get-publication', views.get_publication, name='get-publication'),
]
