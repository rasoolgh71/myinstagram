from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class instagarm_login(models.Model):
    username = models.CharField(max_length=90)
    password = models.CharField(max_length=90)
    last_login = models.DateTimeField(blank=True, null=True)
    #settings=models.ForeignKey(Settings,on_delete=models.CASCADE)
    #def __str__(self):
       # return (self.username)
@python_2_unicode_compatible
class instagram_follower(models.Model):
    pk_follower = models.CharField(max_length=20)
    username = models.CharField(max_length=40)

@python_2_unicode_compatible
class Settings(models.Model):
    follow = models.BooleanField(default=False)
    unfollow = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    #name_user = models.ForeignKey(instagarm_login,on_delete=models.CASCADE)

    #def __str__(self):
     #   return (self.follow)