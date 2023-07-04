from django.urls import path
from . import views

urlpatterns = [
    path('api/events/', views.events_list_api_view, name='events_list_api'),
    path('api/event_details/<uuid:pk>/', views.event_details_api_view, name='event_details_api'),
]
