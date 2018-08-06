from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.core import serializers

# Create your models here.
@python_2_unicode_compatible
class Instagarm_login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    last_login = models.DateTimeField(blank=True, null=True)
    follower_count=models.CharField(max_length=12)
    following_count=models.CharField(max_length=12)
    profil_pic_url=models.CharField(max_length=200)
    total_follows=models.CharField(max_length=12)
    user_id = models.CharField(max_length=15)
    #setting=models.ForeignKey("Setting",on_delete=models.CASCADE)
    def __str__(self):
        return self.username

@python_2_unicode_compatible
class Instagram_follower(models.Model):
   pk_follower = models.CharField(max_length=20)
   username = models.CharField(max_length=40)
   user_id1 = models.ForeignKey("Instagarm_login",on_delete=models.CASCADE)

@python_2_unicode_compatible
class Setting(models.Model):
    follow = models.BooleanField(default=False)
    unfollow = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    userid = models.ForeignKey("Instagarm_login",on_delete=models.CASCADE)
