from django.db import models
from header.models import Header

# Create your models here.
class LinksHeader(models.Model):
    header = models.ForeignKey(Header,related_name='link_header', on_delete=models.CASCADE)
    title = models.TextField(default='')
    icon = models.URLField(default='')
    link = models.TextField(default='')
