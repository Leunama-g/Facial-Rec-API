import dataclasses
import datetime
import jwt
from typing import TYPE_CHECKING
from django.conf import settings
from . import models
from django.shortcuts import get_object_or_404

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    phone: str
    clearance_lvl: str
    middle_name: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            clearance_lvl=user.clearance_lvl,
            middle_name=user.middle_name,
            id=user.id,
        )
    
@dataclasses.dataclass
class UserUpdateDataClass:
    first_name: str
    last_name: str
    email: str
    phone: str
    clearance_lvl: str
    middle_name: str
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            clearance_lvl=user.clearance_lvl,
            middle_name=user.middle_name,
            id=user.id,
        )



def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = models.User(
        first_name=user_dc.first_name, 
        last_name=user_dc.last_name, 
        email=user_dc.email,
        middle_name=user_dc.middle_name,
        clearance_lvl=user_dc.clearance_lvl,
        phone=user_dc.phone
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)

def update_user(user_data: "UserUpdateDataClass", user_id) -> "UserDataClass":
    user = get_object_or_404(models.User, pk=user_id)

    user.first_name = user_data.first_name
    user.middle_name = user_data.middle_name
    user.last_name = user_data.last_name
    user.email = user_data.email
    user.clearance_lvl = user_data.clearance_lvl
    user.phone = user_data.phone
    
    user.save()

    return UserDataClass.from_instance(user=user)

def get_users() -> list["UserDataClass"]:
    users = models.User.objects.filter()

    return [
        UserDataClass.from_instance(single_user) for single_user in users
    ]

def user_email_selector(email: str) -> "User":
    user = models.User.objects.filter(email=email).first()

    return user


def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
