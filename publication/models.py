from django.db import models
from django.db.models import DO_NOTHING
from datetime import datetime
import uuid
from account.models import User

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
    doi = models.CharField(max_length=255, unique=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"{self.title}"
        


        

        

    
