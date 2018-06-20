from django.contrib import admin

# Register your models here.
from task.models import instagarm_login,Settings,instagram_follower
admin.site.register(instagarm_login)
admin.site.register(Settings)
admin.site.register(instagram_follower)