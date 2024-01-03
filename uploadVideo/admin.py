from django.contrib import admin
from .models import UploadedVideo, Subs

# Register your models here.

admin.site.register(UploadedVideo)
admin.site.register(Subs)