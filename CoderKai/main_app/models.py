from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Interest(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Motivation(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CoderKaiPoints(models.Model):
    points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest)
    motivations = models.ManyToManyField(Motivation)
    about_me = models.TextField(max_length=64)

# TODO - associated a range of points with a RANK to be displayed on the profile page
# class CoderKaiRank(models.Model):
#     coderkai_rank = models.CharField(default="Code Cadet")
#     points = models.ForeignKey(CoderKaiPoints, on_delete=models.CASCADE)
