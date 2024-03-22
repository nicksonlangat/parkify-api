from django.urls import path

from .views import UserLoginApi, UserRegisterApi, UsersMe

urlpatterns = [
    path("register/", UserRegisterApi.as_view(), name="register"),
    path("login/", UserLoginApi.as_view(), name="login"),
    path("users/me", UsersMe.as_view(), name="me"),
]
