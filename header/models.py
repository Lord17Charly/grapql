from django.db import models
from django.conf import settings

class Header(models.Model):
    title = models.CharField(max_length=255)
    profile_img = models.URLField(blank=True, null=True)
    about = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    posted_by = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='header')
