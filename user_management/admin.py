from django.contrib import admin
from django.contrib.auth.models import User,Group,Permission
from user_management import models

# Register your models here.



class UsersAdmin(admin.ModelAdmin):
    list_filter = ( 'email',)
    search_fields = ('first_name', 'last_name', 'email','username','user_type',)


admin.site.register(models.User, UsersAdmin)

admin.site.unregister(Group)
