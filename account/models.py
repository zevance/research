import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    position = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Profile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    specialization = models.CharField(max_length=250)
    research_interests = models.TextField()
    qualification = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField()
    image = models.ImageField(upload_to='profiles/')