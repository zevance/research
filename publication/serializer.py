from . models import Publication
from rest_framework.serializers import ModelSerializer


class PublicationSerializer(ModelSerializer):
    class Meta:
        model = Publication()
        fields = ['id', 'title', 'abstract']