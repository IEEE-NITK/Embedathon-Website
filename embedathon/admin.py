from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class TeamAdmin(admin.ModelAdmin):
    list_display = ['teamname', 'passcode', 'leader', 'points', 'max_task_visible', 'disqualified']
    list_filter = ['teamname', 'max_task_visible', 'disqualified']
    search_fields = ['teamname', 'passcode']
    ordering = ['-points']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['team', 'city', 'state', 'pincode']
    list_filter = ['team', 'city', 'state']
    search_fields = ['city', 'state', 'pincode']
    ordering = ['state']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'points', 'deadline', 'date_created']
    list_filter = ['title', 'deadline']
    search_fields = ['title']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'task', 'score']
    list_filter = ['team', 'task']
    search_fields = ['team', 'task']

class MyUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "college_name", "ieee_number", "is_verified")
    list_filter = ("is_staff", "is_nitk", "is_active", "groups")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "phone", "college_name", "ieee_number", "is_nitk", "is_verified")}),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Score, ScoreAdmin)
