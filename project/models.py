from django.db import models
from datetime import datetime
from django.db.models import DO_NOTHING
import uuid

# Create your models here.
class Donor(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_address = models.TextField()
    contact_number = models.IntegerField()
    country = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name}"

class Partner(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.name}"

class Role(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4) 
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.name}"

class Member(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete= DO_NOTHING)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.first_name}"

class Project(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    donor = models.ManyToManyField(Donor)
    partner = models.ManyToManyField(Partner)
    member = models.ManyToManyField(Member)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_name = models.FileField(upload_to='project_documents/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.title}"
