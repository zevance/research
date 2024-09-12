from django.db import models
from account.models import User
import uuid
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name='submitted_by',on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField(User, blank =True)
    event_type = models.CharField(max_length=255)
    venue = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    presenter = models.CharField(max_length=255,blank=True)
    presenter_position = models.CharField(max_length=255,blank=True)
    presenter_organisation = models.CharField(max_length=255,blank=True)
    meeting_id = models.CharField(max_length=255,blank=True)
    passcode = models.CharField(max_length=255,blank=True)
    link = models.CharField(max_length=500,blank=True)
    image = models.ImageField(upload_to="events/", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #delivery_mode = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class News(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255)
    tag_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    attachment = models.FileField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"