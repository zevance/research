from . models import Publication
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

class PublicationSerializer(ModelSerializer):
    author = UserSerializer(read_only=True) 
    project = ProjectSerializer(read_only=True)
    class Meta:
        model = Publication
        fields = ['id','co_authors','title', 'abstract','journal_name','publisher','publication_type',
        'year_of_publication','number_of_pages','volume','license','collection','doi','is_approved',
        'image_path','response','reason_for_denial','created_at','author', 'project']

class ResearcherSerializer(ModelSerializer):
    researcher = UserSerializer(read_only=True)
    publication = PublicationSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','position','researcher','publication']