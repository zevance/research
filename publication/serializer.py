from . models import Collection
from rest_framework.serializers import ModelSerializer


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name']
