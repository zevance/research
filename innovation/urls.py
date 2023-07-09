from django.urls import path
from . import views

urlpatterns = [ 
    path('innovations/',views.innovation_list_view , name='innovations'),
    path('innovation_details/<uuid:pk>/', views.innovation_details_view, name='innovation_details'),
    
    path('api/innovations/', views.innovations_api_view, name='innovations_api_list'),
    path('api/innovation_details/<uuid:pk>/', views.innovation_details_api_view, name='innovation_details_api'),
]
