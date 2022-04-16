from asyncio import proactor_events
from cgitb import reset
from email.policy import default
from hashlib import blake2b
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
VOTE_CHOICES = (
        (1, "Like"),
        (-1, "Disike"),
    )


class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return ("Post Object("+str(self.id)+")->"+self.title)
    
    @property
    def liked_users(self):
        result = []
        likes = Vote.objects.filter(post=self, vote=1)
        for like in likes:
            result.append(like.user)
        return result
    
    @property
    def disliked_users(self):
        result = []
        likes = Vote.objects.filter(post=self, vote=-1)
        for like in likes:
            result.append(like.user)
        return result
    
    @property
    def number_of_likes(self):
        return len(self.liked_users)

    @property
    def number_of_dislikes(self):
        return len(self.disliked_users)


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


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='vote',  on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='vote', on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES, blank=False)

    class Meta:
        unique_together = ('user', 'post')