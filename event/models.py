from django.db import models
from account.models import User
import uuid
# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    meeting_type = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'