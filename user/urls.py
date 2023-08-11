from django.urls import path

from . import apis
from  rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("register/", apis.RegisterApi.as_view(), name="register"),
    path("login/", apis.LoginApi.as_view(), name="login"),
    path("me/", apis.UserApi.as_view(), name="me"),
    path("user/<int:user_id>/", apis.UserUpdate.as_view(), name="user"),
    path("user/", apis.UsersRet.as_view(), name="getUsers"),
    path("logout/", apis.LogoutApi.as_view(), name="logout"),
    path("userpass/<int:user_id>/", apis.ChangePassword.as_view(), name="change user password")
]
