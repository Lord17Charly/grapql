from django.db import models
from django.conf import settings
from graphql.pyutils import description
from work_experiencie.models import WorkEperiencies

# Create your models here.
class WorkExperienciesArchivements(models.Model):
    work_experiencies = models.ForeignKey(WorkEperiencies,related_name='archivements', on_delete=models.CASCADE)
    description = models.TextField(default='')
