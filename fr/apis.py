from rest_framework import views
from rest_framework import response

from . import serializer as fr_serializer
from . import services as fr_services
from target import services as targte_services
from target import models as target_models
from . import models as fr_models

from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from core.urls import face_encodings
from core.urls import target_ids
import numpy as np
import face_recognition
import datetime




#create camera // done

#create alert
#   - face id = -1
#       - target not important
#       - target important 
#   - face id exists

class CameraCreateApi(views.APIView):

    def post(self, request):
        serializer = fr_serializer.CameraSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = fr_services.register_camera(data=data)

        return response.Response(data=serializer.data)

    def get(self, request):
        camera_collection = fr_services.get_cameras()

        serializer = fr_serializer.CameraSerializer(camera_collection, many=True)
        return response.Response(data=serializer.data)
    

class CameraStatusUpdateApi(views.APIView):
    def put(self, request, camera_id):
        serializer = fr_serializer.CameraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        camera = serializer.validated_data
        serializer.instance = fr_services.update_camera(
             camera_id=camera_id, camera_data=camera
        )
        res = "Camera: " + str(camera_id) + " has been updated"
        return response.Response(data=res)

noti = [0]

class AlertCreateAPi(views.APIView):
    
    parser_classes = [MultiPartParser]

    def get(self, request):
        alert_collection = fr_services.get_alerts()

        serializer = fr_serializer.AlertSerializer(alert_collection, many=True)
        return response.Response(data=serializer.data)
    
    def post(self, request):        
        #print(request.data)
        global noti
        cam = get_object_or_404(fr_models.Camera, pk=request.data["camera"])
        
        if cam.active == False:
            res = {"id" : -1}
            return response.Response(data=res)
        if request.data["target"] == "-1":
            new_face = face_recognition.load_image_file(request.data["facePicLocation"])
            new_face_encoding = face_recognition.face_encodings(new_face)[0]
            matches = face_recognition.compare_faces(face_encodings,new_face_encoding)
            
            face_distances = face_recognition.face_distance(face_encodings,new_face_encoding)
            target_id = -1
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                target_id = target_ids[best_match_index]
            
            if target_id == -1:
                res = {"id" : -1}
                return response.Response(data=res)
            else:
                req_data = {
                    "camera" : request.data["camera"], 
                    "target" : target_id, 
                    "rec_time" : request.data["rec_time"],
                    "facePicLocation" : request.data["facePicLocation"]
                }
                serializer = fr_serializer.AlertSerializer()
                serializer.instance = fr_services.register_alert(data=req_data)
                noti[0] += 1
                
                return response.Response(data={"id" : serializer.instance.target.id})
            
        else:
            req_data = {
                "camera" : request.data["camera"], 
                "target" : request.data["target"], 
                "rec_time" : request.data["rec_time"],
                "facePicLocation" : request.data["facePicLocation"]
            }
            serializer = fr_serializer.AlertSerializer()
            serializer.instance = fr_services.register_alert(data=req_data)
            noti[0] += 1
           
            
            return response.Response(data={"id" : serializer.instance.target.id})        

class TargetAlertAPI(views.APIView):
    def get(self, request, target_id):
        alert_collection = fr_services.get_target_alert(target_id=target_id)
        serializer = fr_serializer.AlertSerializer(alert_collection, many=True)
        return response.Response(data=serializer.data)


