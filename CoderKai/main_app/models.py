from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Motivation(models.Model):
    users = models.ManyToManyField(
        User, related_name='motivations', blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Interest(models.Model):
    users = models.ManyToManyField(
        User, related_name='interests', blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
