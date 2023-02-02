from django.db import models
from django.db.models import DO_NOTHING
from datetime import datetime
import uuid
from account.models import User

# Create your models here.
class Collection(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.name}"
    
class PublicationType(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.name}"
    
class License(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.name}"
    
    
class Publication(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    collection = models.ForeignKey(Collection, on_delete=DO_NOTHING)
    publication_type = models.ForeignKey(PublicationType, on_delete=DO_NOTHING)
    license = models.ForeignKey(License, on_delete=DO_NOTHING)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_link = models.CharField(max_length=255, unique=True)
    year_of_publication = models.IntegerField()
    place_of_publication = models.CharField(max_length=255)
    isbn = models.CharField(max_length=255, unique=True)
    publisher = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.title}"
    
class Innovation(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.CharField(max_length=255)
    patent = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.title}"

class InnovationMedia(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    innovation = models.ForeignKey(Innovation, on_delete=DO_NOTHING)
    media = models.FileField(upload_to='innovation_media/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.innovation}"
    
class AuthorRank(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.name}"
    
class AuthorType(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.name}"
        
class Researcher(models.Model):
    id = models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=DO_NOTHING)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self):
        return f"{self.user}"
    
class ResearcherInnovation(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    researcher = models.ForeignKey(Researcher,on_delete=DO_NOTHING)
    innovation = models.ForeignKey(Innovation,on_delete=DO_NOTHING)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.researcher}" + f"{self.innovation}"
    
class ResearcherPublication(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    researcher = models.ForeignKey(Researcher, on_delete=DO_NOTHING)
    publication = models.ForeignKey(Publication, on_delete=DO_NOTHING)
    author_type = models.ForeignKey(AuthorType, on_delete=DO_NOTHING)
    author_rank = models.ForeignKey(AuthorRank, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(
        default=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.researcher}" + f"{self.publication}"
    


