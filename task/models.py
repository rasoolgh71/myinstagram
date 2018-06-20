from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.core import serializers

# Create your models here.
@python_2_unicode_compatible
class instagarm_login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    last_login = models.DateTimeField(blank=True, null=True)
    follower_count=models.CharField(max_length=12)
    following_count=models.CharField(max_length=12)
    profil_pic_url=models.CharField(max_length=200)
    total_follows=models.CharField(max_length=12)
    user_id = models.CharField(max_length=15)

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return instagarm_login.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.last_login = validated_data.get('last_login', instance.last_login)
    #     instance.follower_count = validated_data.get('follower_count', instance.follower_count)
    #     instance.following_count = validated_data.get('following_count', instance.following_count)
    #     instance.profil_pic_url = validated_data.get('profil_pic_url',instance.profil_pic_url)
    #     instance.total_follows = validated_data.get('total',instance.total_follows)
    #     instance.user_id =validated_data.get('user_id',instance.user_id)
    #     instance.save()
    #     return instance

    #class Meta:
        #unique_together = ("username", "password","user_id")
    def __str__(self):
        return self.username

    # def save(self):
    #     if not self.pk:
    #         ### we have a newly created object, as the db id is not set
    #         self.date_created = datetime.datetime.now()
    #     super(instagarm_login, self).save()

    #settings=models.ForeignKey(Settings,on_delete=models.CASCADE)
    #def __str__(self):
       # return (self.username)

@python_2_unicode_compatible
class instagram_follower(models.Model):
   pk_follower = models.CharField(max_length=20)
   username = models.CharField(max_length=40)
   user_id = models.ForeignKey("instagarm_login")

@python_2_unicode_compatible
class Settings(models.Model):
    follow = models.BooleanField(default=False)
    unfollow = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    user_id = models.ForeignKey("instagarm_login",on_delete=models.CASCADE)


# class CustomUserDetailsSerializer(serializers):
#
#     is_verified = serializers.SerializerMethodField()
#
#     def get_is_verified(self, user):
#         return (user.username.filter(verified=1).count() > 0)
#
#     class Meta:
#         model = instagarm_login()
#         fields = ('username','password','last_login' 'follower', 'following', 'profil_pic_url','total_follows','user_id')
#
#     def update(self, instance, validated_data):
#         new_username = validated_data.pop('username', None)
#         user = super(CustomUserDetailsSerializer, self).update(instance, validated_data)
#
#         # http://stackoverflow.com/questions/19755102/django-allauth-change-user-email-with-without-verification
#         if new_username:
#             context = self.context
#             request = context.get('request', None)
#             if request:
#                instagarm_login.objects.add_username(request, user, new_username, confirm=True)
#
#         return user