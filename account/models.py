from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from reader.models import Chapter, Manga


class Bookmark(models.Model):
    manga = models.ForeignKey(Manga, verbose_name=_("Манга"), on_delete=models.CASCADE)
    chapter = models.ForeignKey(
        Chapter,
        verbose_name=_("Последняя глава"),
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    profile = models.ForeignKey(
        "Profile",
        related_name="bookmarks",
        verbose_name=_("Профиль"),
        on_delete=models.CASCADE,
    )


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        help_text=_("Выберите пользователя"),
    )
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/", blank=True, verbose_name=_("Фото")
    )

    def __str__(self):
        # return f"Профиль пользователя {self.user.username}"
        return _("Профиль пользователя %(username)s") % {"username": self.user.username}
