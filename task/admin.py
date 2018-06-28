from django.contrib import admin

# Register your models here.
from task.models import Instagarm_login,Instagram_follower,Setting


admin.site.register(Instagram_follower)
admin.site.register(Instagarm_login)
admin.site.register(Setting)