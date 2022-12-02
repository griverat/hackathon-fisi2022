from django.contrib import admin

from .models import Announcement, Topic

# Register your models here.

admin.site.register(Announcement)
admin.site.register(Topic)
