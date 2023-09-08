from django.contrib import admin
from reader.models import *
from parler.admin import TranslatableAdmin

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Manga)
class MangaAdmin(TranslatableAdmin):
    list_display = ['name', 'description']

