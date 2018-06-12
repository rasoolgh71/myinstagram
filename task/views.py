#import client
from django.shortcuts import render, HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView
from .forms import Logininsta
from django.conf import settings
from django.contrib.auth.decorators import login_required
#from instagram import client
# Create your views here.
#from selenium import webdriver
import requests
import json
from myinstagram import bot_insta
import webbrowser
from task.models import instagarm_login
import datetime
from django.utils import timezone
from mylogging import auth_log
from task.models import instagram_follower,Settings
from instabot.bot import bot


#from django.contrib.sessions.backends.cached_db import instagram


tem=''
#following_count=0
#follower_count=0
#username=''
#profile_pic_url=''
#password=""

def home(request):
    return render(request,'task/home.html')


class LoginView(FormView):
    """
    Login user and redirect to setting page

    """

    template_name = 'task/view_login.html'
    success_url = 'task/login/'
    form_class = AuthenticationForm
    #form = Login_view

    def post(self, request):
        #form = Login_view
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            print(username)
            print(password)
            user = authenticate(password=password, username=username)
            if user is not None:
                login(request, user)


                print("login is true")
                #userlogin = self.request.POST['username']
                auth_log.login_auth(username)
                return HttpResponseRedirect('login')
            else:
                #log_error.log_error("login failed")
                return HttpResponseRedirect('/view_login')
            return render(request, 'task/view_login.html')
        except Exception as e:
            print(e)


def login_insta(request):
    global tem
    #global following_count
    #global follower_count
    #global username
   # global profile_pic_url
    #global username
    last_login=datetime.datetime.now()
    print("time is:",last_login)
    form = Logininsta(request.POST)
    if request.method == "POST":
        try:
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            #username1=requests.session().get(username)
            #print("username1:",username1)
            #return HttpResponse(username,password)
            print('username:',username)
            print('password:',password)
            tem = bot.Bot()
            #request.session["username"]=username
            check_login = tem.login(username=username,password=password)
            if (check_login ==True):
                #update data repeate
                count_row_login = instagarm_login.objects.count()
                for i in range(count_row_login):
                    #print("i",i)
                    new_login = instagarm_login(username=username, password=password, last_login=last_login)
                    new_login.save()
                row = instagarm_login.objects.all()
                for r in row:
                    try:
                       instagarm_login.objects.get(username=r.username)
                    except:
                        r.delete()
                # get info instagram
                #following_count=tem.set_following()
                #follower_count=tem.set_follower()
                #profile_pic_url=tem.set_profile_pic()
                #tem.getTotalFollowers()



                return HttpResponseRedirect('/insta')
                #tem.getTotalFollowers(4129588825)

            else:
                print("login is false")
                return HttpResponseRedirect('/login')
        except Exception as e:
            print(e)

    return render(request, 'task/login.html')
    #return render(request, 'task/insta.html',context={username:"usrname"})

def get_insta(request):
    global tem
    #global following_count
    #global follower_count
    #global username
    #global profile_pic_url

    #tem.getTotalFollowers(4129588825)
    #follower=tem.getTotalFollowers1(7035582061)
    # save and check in database
    # for i in range(len(follower[0])):
    #     new_follower = instagram_follower(pk_follower=follower[0][i], username=follower[1][i])
    #     new_follower.save()
    #     row = instagram_follower.objects.all()
    #     for r in row:
    #         if (new_follower == r):
    #             #print(new_follower)
    #             new_follower.delete()

    count_row_follow = instagram_follower.objects.count()
    if request.method == "POST":

        follow=bool(request.POST.get('follow'))
        unfollow =bool(request.POST.get('unfollow'))
        like =bool(request.POST.get('like'))
        comment =bool(request.POST.get('comment'))
        print(type(follow))
        print("follow",follow)
        print("unfollow", unfollow)
        print("like",like)
        print("comment",comment)
        count_row_settings=Settings.objects.count()
        new_setings = Settings(follow=follow, unfollow=unfollow, like=like, comment=comment)
        if(count_row_settings<1):
            new_setings.save()
        else:
            print("else ")
            Settings.objects.update(follow=follow,unfollow=unfollow, like=like, comment=comment)

    p = Settings.objects.all()[0]
    print("folow value:", p.follow)
    value_follow = p.follow
    value_unfollow = p.unfollow
    value_like = p.like
    value_commemnt = p.comment
    #gt=Settings.objects.all()
    #print(gt)
    value_follow=Settings.objects.all()
    #print(value_follow)
    #for i in value_follow:
     #   field_name_val =bool(Settings.objects.get(i.follow))
    if (value_follow == True):
        p1 = instagram_follower.objects.values_list('pk_follower', flat=True)
    field_name_val = bool(getattr(Settings,'follow'))
    print(field_name_val)
    #if(follow1==)

    return render(request,'task/insta.html',context={'value_follow':value_follow,'value_unfollow':value_unfollow,
                                                     'value_like':value_like,'value_commemnt':value_commemnt})


