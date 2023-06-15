from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.innovation_list_view , name='innovations'),
    path('innovation-details/<uuid:pk>', views.innovation_details_view, name='innovation-details'),    
]
