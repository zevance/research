from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EventsSerializer
from .models import Event

# Create your views here.
class EventsListView(APIView):
    def get(self, request, *args, **kwargs):
        instance = Event.objects.all()
        data = {}
        if instance:
            data = EventsSerializer(instance, many = True).data
        return Response(data)

events_list_api_view = EventsListView.as_view()

class EventDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(id =pk)
        except Event.DoesNotExist:
            return Response('Event does not exist...!!!!')
        
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventsSerializer(event, many=False)
        return Response(serializer.data)

event_details_api_view = EventDetailsAPIView.as_view()