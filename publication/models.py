from django.db import models
from django.db.models import DO_NOTHING
from datetime import datetime
import uuid
from account.models import User
from project.models import UmbrellaProject

# Create your models here.    
class Publication(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=DO_NOTHING)
    co_authors = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    journal_name = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_type = models.CharField(max_length=255)
    year_of_publication = models.IntegerField()
    number_of_pages = models.CharField(max_length=255,blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    license = models.CharField(max_length=255)
    collection = models.CharField(max_length=255)
    doi = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    image_path = models.ImageField(upload_to='publication/', blank=True, null=True)
    project = models.ForeignKey(UmbrellaProject, on_delete=DO_NOTHING, blank=True, null=True)
    response = models.BooleanField(blank=True,null=True)
    reason_for_denial = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
        
    def __str__(self):
        return f"{self.title}"
      
    def get_absolute_url(self):
        return reverse('author_view', args=[str(self.pk)])
        
class Publication_Author(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    publication = models.ForeignKey(Publication, on_delete=DO_NOTHING)
    author = models.ForeignKey(User, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.publication} {self.author}"
    

        

        

    
