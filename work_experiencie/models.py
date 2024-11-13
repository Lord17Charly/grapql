from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.timezone import now

class WorkEperiencies(models.Model):
    company = models.TextField(default='')
    position = models.TextField(default='')
    location = models.TextField(default='')
    start_date = models.DateField(default=now,blank=True)
    end_date = models.DateField(default=now,blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                null=True,on_delete=models.CASCADE)
