from email.policy import default
from hashlib import blake2b
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.JSONField(default=dict, blank=True, null=True)
    dislikes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='postimage', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='PostImages')
    

class Tag(models.Model):
    text = models.CharField(max_length=15)

    def __str__(self):
        return self.text


class PostTag(models.Model):
    post = models.ForeignKey(Post, related_name='posttag', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return self.tag.text