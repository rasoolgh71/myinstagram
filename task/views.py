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
import datetime
from django.utils import timezone
from mylogging import auth_log
from task.models import Instagarm_login,Setting,Instagram_follower
from instabot.bot import bot


tem=''

def home(request):
    return render(request,'task/home.html')


class LoginView(FormView):
    """
    Login user and redirect to setting page

    """

    template_name = 'task/view_login.html'
    success_url = 'task/login/'
    form_class = AuthenticationForm

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
                auth_log.login_auth(username)
                return HttpResponseRedirect('login')
            else:
                return HttpResponseRedirect('/view_login')
            return render(request, 'task/view_login.html')
        except Exception as e:
            print(e)


def login_insta(request):
    global tem
    last_login=datetime.datetime.now()
    print("time is:",last_login)
    form = Logininsta(request.POST)
    if request.method == "POST":
        try:
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            print('username:',username)
            print('password:',password)
            tem = bot.Bot()
            request.session["username"]=username
            check_login = tem.login(username=username,password=password)
            if (check_login ==True):
                user_id=tem.get_user_id_from_username(username)
                print("user_id",user_id)
                profil_pic_url=tem.get_profile_pic_url(user_id)
                print("profil_pic_url",profil_pic_url)
                follower_count=tem.get_follower_count(user_id)
                print("follower_count",follower_count)
                following_count=tem.get_following_count(user_id)
                print("following_count",following_count)
                total_follows=tem.total['follows']
                print("totol",total_follows)

                count_row_login = Instagarm_login.objects.count()
                row_login=Instagarm_login.objects.all()


                new_login = Instagarm_login(username=username, password=password, last_login=last_login,
                                            following_count=following_count, follower_count=follower_count,
                                            profil_pic_url=profil_pic_url, total_follows=total_follows,
                                            user_id=user_id)

                created=Instagarm_login.objects.filter(user_id=user_id).exists()
                print("created:",created)
                if created:

                    print(" user exisit,update user ")
                    Instagarm_login.objects.filter(username=username).update(username=username, password=password,
                                                                             last_login=last_login,
                                                                             following_count=following_count,
                                                                             follower_count=follower_count,
                                                                             profil_pic_url=profil_pic_url,
                                                                             total_follows=total_follows,
                                                                             user_id=user_id)
                else:
                    print("user no exixit,new user create")
                    new_login.save()
                    new_setting = Setting(follow=False, unfollow=False, like=False, comment=False,
                                          userid=Instagarm_login.objects.get(username=username))
                    new_setting.save()
                return HttpResponseRedirect('/insta')
            else:

                return HttpResponseRedirect('/login')
        except Exception as e:
            print(e)
    return render(request, 'task/login.html')

def get_insta(request):
    global tem
    username = request.session["username"]
    #tem.getTotalFollowers(4129588825)
    user_id = tem.get_user_id_from_username(username)
    follower=tem.get_user_followers(user_id)
    #print(follower)
    # save and check in database
    #for i in follower:
        #print(i)
        #new_follower = Instagram_follower(pk_follower=i, username=tem.get_username_from_user_id(i))
        #print(i)
        #print(tem.get_username_from_user_id(i))
        # new_follower.save()
    #     row = instagram_follower.objects.all()
    #     for r in row:
    #         if (new_follower == r):
    #             #print(new_follower)
    #             new_follower.delete()
    #username = request.session["username"]
    print("username sesson:", username)
    user_login=Instagarm_login.objects.filter(username=username)
    print(user_login)
    #print(user_login.profil_pic_url)

    return render(request, 'task/insta.html',{'user_login':user_login})

def settings(request):
    username = request.session["username"]
    print("username sesson settings:", username)

    if request.method == "POST":
        username = request.session["username"]
        follow = bool(request.POST.get('follow'))
        unfollow = bool(request.POST.get('unfollow'))
        like = bool(request.POST.get('like'))
        comment = bool(request.POST.get('comment'))
        print(type(follow))
        print("follow", follow)
        print("unfollow", unfollow)
        print("like", like)
        print("comment", comment)
        count_row_settings = Setting.objects.count()
        row_settigngs = Setting.objects.all()
        user_name = Instagarm_login.objects.get(username=username)
        print("user_name :",username)
        new_setings = Setting(follow=follow, unfollow=unfollow, like=like, comment=comment,
                               userid=Instagarm_login.objects.get(username=username))

        created = Setting.objects.filter(userid=Instagarm_login.objects.get(username=username)).exists()
        if created:
            print(" user exisit,update user ")
            Setting.objects.filter(userid=Instagarm_login.objects.get(username=username)).update(follow=follow,
                                                                unfollow=unfollow,
                                                                like=like,
                                                                comment=comment,
                                                                userid=Instagarm_login.objects.get(username=username))
        else:
            print("settings no exixit,new settings create")
            new_setings.save()
        value = Setting.objects.get(userid=Instagarm_login.objects.get(username=username))

    value = Setting.objects.get(userid=Instagarm_login.objects.get(username=username))
    print("value is:", value)
    print("value follow", value.follow)
    print("value unfollow", value.unfollow)
    print("value like", value.like)
    print("value comment:", value.comment)
    value_follow = value.follow
    value_unfollow = value.unfollow
    value_like = value.like
    value_comment = value.comment
    return render(request,'task/settings.html',context={'value_follow': value_follow,
                                                          'value_unfollow': value_unfollow,
                                                          'value_like': value_like,


                                                          'value_comment': value_comment})
def save1():
    print("save in folllower")

def follows(request):
    return render(request,'task/follows.html')