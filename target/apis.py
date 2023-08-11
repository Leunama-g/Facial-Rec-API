from rest_framework import views
from rest_framework import permissions
from rest_framework import response
from rest_framework import status as rest_status
from rest_framework.parsers import MultiPartParser
from user import authentication
from . import serializer as Target_serializer
from . import services

from core.urls import face_encodings
from core.urls import target_ids
import face_recognition
import os
from core import settings

media_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'mediafiles')


class TargetCreateApi(views.APIView):
    
    parser_classes = [MultiPartParser]
    def post(self, request):
        serializer = Target_serializer.TargetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
    
        serializer.instance = services.register_Target(data=data)
        pic_loc = media_path + "\\" + str(serializer.instance.facePicLocation).replace('/', '\\')
        
        try:
            face_encodings.append(face_recognition.face_encodings(face_image=face_recognition.load_image_file(pic_loc))[0])
            target_ids.append(serializer.instance.id)
        except IndexError:
            serializer.instance.active = False
            serializer.instance = services.update_target(target_id=serializer.instance.id, target_data=serializer.instance)
            print("face was not encoded")
        else:
            print("face encoded")
        return response.Response(data=serializer.data)

    def get(self, request):
        Target_collection = services.get_Targets()

        serializer = Target_serializer.TargetSerializer(Target_collection, many=True)
        return response.Response(data=serializer.data)


class TargetRetrieveUpdate(views.APIView):
   

    def get(self, request, target_id):
        target = services.get_target_detail(target_id=target_id)
        serializer = Target_serializer.TargetSerializer(target)
        return response.Response(data=serializer.data)

    def put(self, request, target_id):
        serializer = Target_serializer.TargetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target = serializer.validated_data
        serializer.instance = services.update_target(
             target_id=target_id, target_data=target, target_ids=target_ids, face_encodings=face_encodings
        )

        return response.Response(data=serializer.data)