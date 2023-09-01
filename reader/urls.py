from django.urls import path, include
from .views import *


urlpatterns = [
    path("", landing_view, name="landing"),
    path("bookmarks", bookmarks, name="bookmarks"),
    path("contact", contact, name="contact"),
    path("mangas", MangaListView.as_view(), name="manga_list"),
    path("chapter_user_action", chapter_action, name="chapter_user_action"),
    path("<slug:manga_slug>/", chapter_list, name="chapter_list"),
    path(
        "<slug:manga_slug>/most_viewed_chapters",
        most_viewed_chapters,
        name="most_viewed_chapters",
    ),
    path(
        "<slug:manga_slug>/<slug:chapter_slug>/",
        ChapterDetail.as_view(),
        name="chapter_detail",
    ),
]
