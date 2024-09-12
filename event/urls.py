from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list_view, name='news'),
    path('news_details/<uuid:pk>/', views.news_details_view, name='news_details'),
    path('event_details/<uuid:pk>/', views.event_details, name='event_details'),
    path('api/events/', views.events_list_api_view, name='events_list_api'),
    path('api/event_details/<uuid:pk>/', views.event_details_api_view, name='event_details_api'),
]
