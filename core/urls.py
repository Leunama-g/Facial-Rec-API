"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import face_recognition
from target.models import Target
from target.services import TargetDataClass,update_target
from . import settings
import os

face_encodings = []
target_ids = []


def load_faces():
    targets = [
        TargetDataClass.from_instance(single_Target) for single_Target in Target.objects.filter(active=True)
    ]
    media_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'mediafiles')
    for target in targets:
        pic_loc = media_path + "\\" + str(target.facePicLocation).replace('/', '\\')
        face_image = face_recognition.load_image_file(pic_loc)
        try:
            face_encodings.append(face_recognition.face_encodings(face_image=face_image)[0])
            target_ids.append(target.id)
        except IndexError: 
            print("Cant encode for " + str(target.id))
        else:
            print("face encoded")
    print(len(face_encodings))

load_faces()

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("user.urls")),
    path("api/", include("target.urls")),
    path("api/", include("fr.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


