from django.db import models
from django.db.models import DO_NOTHING
from datetime import datetime
import uuid
from account.models import User
from project.models import UmbrellaProject

# Create your models here.
class Innovation(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField()
    patent = models.CharField(max_length=255)
    year_of_innovation = models.IntegerField()
    image_path = models.ImageField(upload_to='innovations/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    project = models.ForeignKey(UmbrellaProject, on_delete=DO_NOTHING ,blank=True, null=True)
    response = models.BooleanField(blank=True,null=True)
    reason_for_denial = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"