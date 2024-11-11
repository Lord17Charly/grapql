from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.timezone import now



class Education(models.Model):
    degree = models.TextField(default='')
    university = models.TextField(default='')
    star_data = models.DateField(default=now,blank=True)
    end_data = models.DateField(default=now,blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                null=True,on_delete=models.CASCADE)
