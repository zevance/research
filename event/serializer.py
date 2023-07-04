from rest_framework.serializers import ModelSerializer
from .models import Event

class EventsSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'