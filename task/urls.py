from django.conf.urls import url
from . import views
from .views import LoginView

app_name = 'task'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.login_insta, name='login'),
    url(r'^insta$', views.get_insta, name='insta'),
    url(r'^settings$', views.settings, name='settings'),
    url(r'^follows$', views.follows, name='follows'),

    #url(r'^view_login$', views.view_login, name='view_login'),
    url(r'^view_login$', LoginView.as_view(), name='view_login'),


    #url(r'^https://t.me/bot1stets$', views.join_telegram, name='telegram'),

]