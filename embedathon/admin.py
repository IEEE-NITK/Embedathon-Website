from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ExportMixin

from .models import *

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        exclude = ('passcode', 'date_created')

class TeamAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['teamname', 'passcode', 'leader', 'points', 'max_task_visible', 'disqualified']
    list_filter = ['teamname', 'max_task_visible', 'disqualified']
    search_fields = ['teamname', 'passcode']
    ordering = ['-points']
    resource_classes = (TeamResource,)

class AddressResource(resources.ModelResource):
    class Meta:
        model = Address

class AddressAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['team', 'city', 'state', 'pincode']
    list_filter = ['team', 'city', 'state']
    search_fields = ['city', 'state', 'pincode']
    ordering = ['state']
    resource_classes = (AddressResource,)

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task

class TaskAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'title', 'points', 'deadline', 'date_created']
    list_filter = ['title', 'deadline']
    search_fields = ['title']
    resource_classes = (TaskResource,)

class ScoreResource(resources.ModelResource):
    class Meta:
        model = Score

class ScoreAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['id', 'team', 'task', 'score']
    list_filter = ['team', 'task']
    search_fields = ['team', 'task']
    resource_classes = (ScoreResource,)

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'phone', 'ieee_number', 'college_name')

class MyUserAdmin(ExportMixin, UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "college_name", "ieee_number", "is_staff")
    list_filter = ("is_staff", "is_nitk", "is_active", "groups")
    resource_classes = (UserResource,)

admin.site.register(User, MyUserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Score, ScoreAdmin)
