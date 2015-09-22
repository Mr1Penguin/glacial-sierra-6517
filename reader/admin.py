from django.contrib import admin

# Register your models here.
from .models import User, Site

admin.site.register(User)
admin.site.register(Site)