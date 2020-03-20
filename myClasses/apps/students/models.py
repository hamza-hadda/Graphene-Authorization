from django.db import models
from apps.profs.apps import ProfsConfig

# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=100)
