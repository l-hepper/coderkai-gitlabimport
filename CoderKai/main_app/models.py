from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Interest(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)


class Motivation(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)


