"""Admin"""
import pprint
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Pontiff

from django.contrib.sessions.models import Session

class PontiffAdmin(admin.ModelAdmin):
    list_display = ('papal_name', 'first_name', 'last_name', 'begin', 'finish')

admin.site.register(Pontiff, PontiffAdmin)
