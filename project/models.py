from django.db import models
from datetime import datetime
from django.db.models import DO_NOTHING
from publication.models import Publication
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
    email = models.EmailField()
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
    email = models.EmailField()
    role = models.OneToOneField(Role, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.first_name}"

class Project(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    #total_value = models.DecimalField(max_digits=50,decimal_places=3)
    #project_status = models.CharField(max_length=255)
    donor = models.ManyToManyField(Donor)
    partner = models.ManyToManyField(Partner)
    member = models.ManyToManyField(Member)
    publication = models.ManyToManyField(Publication, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_name = models.FileField(upload_to='project_documents/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(
        default=datetime.now)

    def __str__(self):
        return f"{self.title}"
