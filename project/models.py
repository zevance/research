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

class Project(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"

class DonorProjects(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    donor = models.ForeignKey(Donor, on_delete= DO_NOTHING)
    project = models.ForeignKey(Project, on_delete= DO_NOTHING)

    def __str__(self):
        return f"{self.donor}" + f"{self.project}"

class Member(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name}"

class Partner(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class ProjectPartners(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    project = models.ForeignKey(Project, on_delete= DO_NOTHING)
    partner = models.ForeignKey(Partner, on_delete= DO_NOTHING)

    def __str__(self):
        return f"{self.partner}" + f"{self.project}"

class Role(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4) 
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class ProjectMembers(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    project = models.ForeignKey(Project, on_delete= DO_NOTHING)
    member = models.ForeignKey(Member, on_delete= DO_NOTHING)
    role = models.ForeignKey(Role, on_delete= DO_NOTHING)

    def __str__(self):
        return f"{self.member}" + f"{self.project}" + f"{self.role}"

class ProjectDocuments(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    project = models.ForeignKey(Project, on_delete= DO_NOTHING)
    file_name = models.FileField(upload_to='project_documents/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f"{self.project}"