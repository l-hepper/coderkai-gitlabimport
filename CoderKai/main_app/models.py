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
    

class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class TypeTag(models.Model):
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
    avatar = models.ImageField(upload_to="images", default="images/default-avatar.png", null=True, blank=True)
    interests = models.ManyToManyField(Interest)
    motivations = models.ManyToManyField(Motivation)
    about_me = models.TextField(max_length=64)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64)
    body = models.TextField(max_length=2048)
    preview = models.CharField(max_length=512)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    coderkaipoints = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag)
    type_tag = models.ForeignKey(TypeTag, on_delete=models.SET_NULL, null=True, blank=True)

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)
    coderkaipoints = models.IntegerField(default=1)


class Reply(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)


class PostKudos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']


class ResponseKudos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'response']


class KaiGroup(models.Model):
    name = models.CharField(max_length=20, unique=True)
    about = models.TextField(max_length=252, help_text="Short info about the group")
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_groups")
    members = models.ManyToManyField(User)
    interests = models.ManyToManyField(Interest)
    motivations = models.ManyToManyField(Motivation)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name



# TODO - associated a range of points with a RANK to be displayed on the profile page
# class CoderKaiRank(models.Model):
#     coderkai_rank = models.CharField(default="Code Cadet")
#     points = models.ForeignKey(CoderKaiPoints, on_delete=models.CASCADE)
