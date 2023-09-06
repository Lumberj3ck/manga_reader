from django.urls import path, include
from .views import search, bookmark

urlpatterns = [
    path("", search, name='search'),
    path("bookmark", bookmark, name='make_bookmark'),
]