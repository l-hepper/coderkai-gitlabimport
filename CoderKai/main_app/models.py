from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class User(models.Model):
    username = models.CharField(max_length=16)
    email = models.EmailField(max_length=60)
    