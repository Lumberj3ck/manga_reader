from enum import unique
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Manga(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название манги"))
    slug = models.SlugField(max_length=200, unique=True)
    poster = models.ImageField(upload_to='manga_poster/', blank=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(
        max_length=200, verbose_name=_("Название главы"), unique=True
    )
    chapter_number = models.PositiveIntegerField(unique=True)
    ## name is unique hence i thought is would be redudant to save both of them slug and name
    # slug = models.SlugField(max_length=200, blank=True)
    manga = models.ForeignKey(
        "Manga", on_delete=models.CASCADE, related_name=_("chapters")
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="liked_chapters",
        verbose_name=_("Понравилось"),
    )

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    """function called every time models img saved"""
    folder_name = instance.chapter.name.replace(" ", "-")
    return os.path.join(folder_name, filename)


class Picture(models.Model):
    chapter = models.ForeignKey(
        "Chapter",
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("Глава"),
    )
    img = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.img.name


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    chapter = models.ForeignKey(
        "Chapter", on_delete=models.CASCADE, verbose_name=_("Глава")
    )
    text = models.CharField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
