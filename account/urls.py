from django.urls import path, include
from .views import UserEditView, UserRegistration


urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("user_edit/", UserEditView.as_view(), name="user_edit"),
    path("", include("django.contrib.auth.urls")),
]
