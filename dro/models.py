from django.db import models
import uuid
from account.models import User

# Create your models here.
class Call(models.Model):
    CATEGORY_CHOICES =[
        ('grant', 'Grant'),
        ('project', 'Project'),
        ('consultancy', 'Consultancy')
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]

    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    document = models.FileField(upload_to='calls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
