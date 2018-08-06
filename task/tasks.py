import datetime
#from __future__ import absolute_import
from celery import shared_task
from instabot.bot import bot
from task.models import Instagarm_login,User,Instagram_follower
from django.shortcuts import render, HttpResponse,HttpResponseRedirect,get_object_or_404

from celery.decorators import task
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
#username=''
import time
from django.utils.crypto import get_random_string
import string

@shared_task
def background1(total):
    while True:
        get_data=get_random_string(50)
        print(get_data)
        print("in the background")
    return '{} random users created with success!'.format(total)

@shared_task
def save_follower(total):
    follower=[]
    get_userid=Instagarm_login.objects.all()
    get_user = Instagarm_login.objects.all().order_by("-last_login")[0:1]

    for data in get_user:
        print(data.username)
        username=data.username
        password=data.password
        print(data.password)

    tem = bot.Bot()
    check_login = tem.login(username=username, password=password)
    if(check_login==True):
        for i in get_user:
            user_id1=i.user_id
            follower=(tem.get_user_followers(i.user_id))

    created1 = Instagarm_login.objects.filter(username=username).exists()
    if(created1):
        print("te user alerady exists in database")
    else:
        for i in follower:
            time.sleep(2) #Delays for 5 seconds.
            created = Instagram_follower.objects.filter(pk_follower=i).exists()
            print("created:", created)
            if created:
                time.sleep(2)
                print(i+ "alredy exists in database")
            else:
                time.sleep(2)
                username = tem.get_username_from_user_id(i)
                new_follower = Instagram_follower(pk_follower=i,username=username,
                                              user_id1=Instagarm_login.objects.get(user_id=user_id1))
                new_follower.save()



#@shared_task
#def name_of_your_function(optional_param):
 #   pass


        # @shared_task(name="health_test")
# def test():
#     print(datetime.datetime.now())
#

    # s = Session.objects.get()
    # session_data = s.get_decoded()
    # uid = session_data.get('_auth_user_id')
    # user = User.objects.get(id=uid)
    # print("user:",user)
    #

    #
    #

    #for i in s:
        #print(i.get_decoded())
    #print(self.request.id)
    #global username
    #get_user=Instagarm_login.objects.filter()
    #for i in get_user:
     #   print(i. username)
    #user = User.objects.get(username=request.user.username)
    #username=request.user.username
    #print("username:"+username)
    #print('username is:'+username)
    #print("hi celery task in time 10 s")
    #return '{} repeat  in one minutes!'.format("rasool")


# @task(name="sum_two_numbers")
# def add(x, y):
#     return x + y


# def get_follower(request):
#     tem1= bot.Bot()
#     request.user.username
#     username=Instagarm_login.objects.filter()
#     check_login1 = tem1.login(username=username, password=password)
#     while True:
        #tem.getTotalFollowers(4129588825)
        #follower=tem.getTotalFollowers1(7035582061)
     #save and check in database
    # for i in range(len(follower[0])):
    #     new_follower = instagram_follower(pk_follower=follower[0][i], username=follower[1][i])
    #     new_follower.save()