from . models import Innovation
from rest_framework.serializers import ModelSerializer
from account.models import User
from project.models import Project

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title']

class InnovationSerializer(ModelSerializer):
    user = UserSerializer(read_only=True) 
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Innovation
        fields = ['id', 'title', 'description','patent','year_of_innovation','image_path','is_approved',
        'created_at','user', 'project']

