from email.policy import default
from hashlib import blake2b
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.JSONField(default=dict, blank=True, null=True)
    dislikes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.user.username
