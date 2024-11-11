from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.timezone import now

class Archievement(models.Model):
    title = models.TextField(default='')
    description = models.TextField(default='')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                null=True,on_delete=models.CASCADE)
