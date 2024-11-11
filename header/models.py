from django.db import models

# Create your models here.
from django.conf import settings
from django.utils.timezone import now


class header(models.Model):
    title = models.TextField(default='')
    profile_img = models.TextField(default='')
    about = models.TextField(default='')
    links = models.TextField(default='')
    created_at = models.DateField
    updated_at = models.DateField
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
    null=True,on_delete=models.CASCADE)
