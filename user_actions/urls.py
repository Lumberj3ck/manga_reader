from django.urls import path, include
from .views import search

urlpatterns = [
    path("", search, name='search'),
]