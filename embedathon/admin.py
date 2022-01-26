from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Address)
admin.site.register(Task)
admin.site.register(Score)
