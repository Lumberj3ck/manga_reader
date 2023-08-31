from django.contrib import admin
from .models import Bookmark, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Bookmark)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('manga', 'chapter', 'profile')
