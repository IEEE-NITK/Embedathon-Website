from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Address)
admin.site.register(Task)
admin.site.register(Score)
