from django.urls import path, include
from .views import UserEditView, UserRegistration, user_login 


urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("user_edit/", UserEditView.as_view(), name="user_edit"),
    path("login/", user_login, name="login"),
    path("", include("django.contrib.auth.urls")),
]
