from django.db import models
from datetime import datetime
from django.db.models import DO_NOTHING
import uuid
from account.models import User

# Create your models here.
class Project(models.Model):
    id            = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user          = models.ForeignKey(User, on_delete=DO_NOTHING)
    title         = models.CharField(max_length=255)
    total_value    = models.DecimalField(max_digits=50,decimal_places=3)
    project_status = models.CharField(max_length=255)
    project_type   = models.CharField(max_length=255)
    project_pi = models.CharField(max_length=255)
    project_co_pi = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date_from = models.DateField()
    expected_completion_date = models.DateField()
    project_member = models.TextField()
    project_donor = models.TextField()
    project_partner = models.TextField(blank=True, null=True)
    description = models.TextField()
    supporting_document = models.FileField(upload_to='project_documents/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.title}"