import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    position = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

