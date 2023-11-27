from rest_framework.serializers import ModelSerializer
from .models import Event, News

class EventsSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'