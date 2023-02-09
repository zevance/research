from . models import Collection, License, PublicationType
from rest_framework.serializers import ModelSerializer


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class LicenseSerializer(ModelSerializer):
    class Meta:
        model = License
        fields = ['id', 'name']

class PublicationTypeSerializer(ModelSerializer):
    class Meta:
        model = PublicationType
        fields = ['id', 'name']