import datetime
from celery import shared_task
from instabot.bot import bot
from task.models import Instagarm_login,User

from celery.decorators import task

username=''

def get_username(request):
    global username
    username=User.objects.get(username=request.user.username)
    return username
    #print("username is:"+username)


@shared_task(name="health_test")
def test():
    global username
    #user = User.objects.get(username=request.user.username)
    #username=request.user.username
    #print("username:"+username)
    print('username is:'+username)
    print("hi celery task in time 10 s")

@task(name="sum_two_numbers")
def add(x, y):
    return x + y


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