from django.db import models
import uuid
from account.models import User
from dro.models import Call

# Create your models here.
class Grant(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    call = models.ForeignKey(Call,on_delete=models.DO_NOTHING, blank=True, null=True)
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
    is_approved = models.BooleanField(default=False, null=True, blank=True)
    reason_for_denial = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
    