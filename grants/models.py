from django.db import models
import uuid
from account.models import User

# Create your models here.
class Grant(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    amount_of_funding = models.FloatField()
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    introduction = models.TextField()
    justification = models.TextField()
    objectives = models.TextField()
    methodology = models.TextField()
    research_dessemination_strategy = models.TextField()
    ethical_considerations = models.TextField()
    budget = models.FileField(upload_to="grants/")
    resume = models.FileField(upload_to ="grants/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    