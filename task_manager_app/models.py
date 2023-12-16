from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title