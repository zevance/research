from . models import Innovation
from rest_framework.serializers import ModelSerializer


class InnovationSerializer(ModelSerializer):
    class Meta:
        model = Innovation()
        fields = '__all__'

