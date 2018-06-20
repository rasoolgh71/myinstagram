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
from task.models import instagarm_login,Settings,instagram_follower
from instabot.bot import bot


#from django.contrib.sessions.backends.cached_db import instagram


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
            print('username:',username)
            print('password:',password)
            tem = bot.Bot()
            request.session["username"]=username
            check_login = tem.login(username=username,password=password)
            if (check_login ==True):
                #update data repeate
                #count_row_login = instagarm_login.objects.count()
                #for i in range(count_row_login):
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

                count_row_login = instagarm_login.objects.count()
                row_login=instagarm_login.objects.all()


                new_login = instagarm_login(username=username, password=password, last_login=last_login,
                                            following_count=following_count, follower_count=follower_count,
                                            profil_pic_url=profil_pic_url, total_follows=total_follows,
                                            user_id=user_id)

                person, created = instagarm_login.objects.get_or_create(user_id=user_id)
                if created:
                    print("user no exixit,new user create")
                    new_login.save()
                else:
                    print(" user exisit,update user ")
                    instagarm_login.objects.filter(user_id=user_id).update(username=username, password=password,
                                                   last_login=last_login,
                                                   following_count=following_count, follower_count=follower_count,
                                                   profil_pic_url=profil_pic_url, total_follows=total_follows,
                                                   user_id=user_id)

                for r in row_login:
                    try:
                        instagarm_login.objects.get(username=r.username)
                    except:
                        r.delete()
                return HttpResponseRedirect('/insta')
            else:

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

    #count_row_follow = instagram_follower.objects.count()
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

        username=request.session["username"]
        #skill = Skill.objects.get(id=skill_id)
        #name_skill = request.POST.get('name_skill', '')

        #user_id = tem.get_user_id_from_username(username)
        #user_pk=instagarm_login.objects.filter(username=username)
        #userid=instagarm_login.bjects.get()
        count_row_settings = Settings.objects.count()
        row_settigngs=Settings.objects.all()
        user_id=instagarm_login.objects.get(username=username)
        new_setings = Settings(follow=follow, unfollow=unfollow, like=like, comment=comment,
                               user_id=instagarm_login.objects.get(username=username))

        if(count_row_settings>0):
            for i in row_settigngs:
                if(i.user_id==user_id):
                    Settings.objects.update(follow=follow, unfollow=unfollow, like=like, comment=comment,
                                            user_id=instagarm_login.objects.get(username=username))
                else:
                    new_setings.save()
        else:
            new_setings.save()

        value = Settings.objects.get(user_id=user_id)
        print("value follow", value.follow)
        print("value unfollow", value.unfollow)
        value_follow=value.follow
        value_unfollow=value.unfollow
        value_like=value.like
        value_comment=value.comment
        return render(request, 'task/insta.html',
                      context={'value_follow': value_follow, 'value_unfollow': value_unfollow,
                               'value_like': value_like, 'value_comment': value_comment})

           # print("folow value:", p.follow)
            #value_follow = p.follow
            #value_unfollow = p.unfollow
            #value_like = p.like
            #value_commemnt = p.comment
    #gt=Settings.objects.all()
    #print(gt)

    #print(value_follow)
    #for i in value_follow:
     #   field_name_val =bool(Settings.objects.get(i.follow))
    #if (value_follow == True):
       # p1 = instagram_follower.objects.values_list('pk_follower', flat=True)
    #field_name_val = bool(getattr(Settings,'follow'))
    #print(field_name_val)
    #if(follow1==)


    return render(request,'task/insta.html')


