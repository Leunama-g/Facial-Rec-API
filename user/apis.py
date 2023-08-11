
from rest_framework import views, response, exceptions, permissions

from . import serializer as user_serializer
from . import services, authentication
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view
from rest_framework.response import responses
from rest_framework import status
from .models import User
from .serializer  import UserSerializer
from requests import Response
from django.shortcuts import get_object_or_404

import string
import secrets

letters = string.ascii_letters
digits = string.digits

alphabet = letters + digits

class RegisterApi(views.APIView):

    parser_classes = [MultiPartParser]
    
    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_user(user_dc=data)

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if user.clearance_lvl == "Level 0":
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)
        resp.data = user_serializer.UserSerializer(user).data
        return resp


class UserApi(views.APIView):
    """
    This endpoint can only be used
    if the user is authenticated
    """


    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(serializer.data)


class LogoutApi(views.APIView):
    

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "so long farewell"}

        return resp
    

class UsersRet(views.APIView):
 

    def get(self, request):
        user_collection = services.get_users()

        serializer = user_serializer.UserSerializer(user_collection, many=True)
        return response.Response(data=serializer.data)

class UserUpdate(views.APIView):


    def put(self, request, user_id):
        serializer = user_serializer.UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.update_user(user_data=data, user_id=user_id)

        return response.Response(data=serializer.data)
        
#change password functionality 
class ChangePassword(views.APIView):
 

    def put(self, request, user_id):
        Npassword = request.data["new_password"]
        Cpassword = request.data["cur_password"]

        user = get_object_or_404(User, pk=user_id)

        if not user.check_password(raw_password=Cpassword):
            raise exceptions.AuthenticationFailed("old password is incorrect")
        
        user.set_password(Npassword)
        user.save()
        
        
        return response.Response(data="password changed")
    
    def post(self, request, user_id):
        pwd = ''
        for i in range(8):
            pwd += ''.join(secrets.choice(alphabet))

        user = get_object_or_404(User, pk=user_id)
        user.set_password(pwd)
        user.save()
        return response.Response(data={"randPass" : pwd})

#reset password functionality 

