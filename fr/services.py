import dataclasses
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from . import models as fr_models
from target import models as target_models
from target import serializer as target_serializer

from target import services as target_services

if TYPE_CHECKING:
    from models import Camera
    from models import Alert
    from target.models import Target

@dataclasses.dataclass
class CameraDataClass:
    active: bool 
    city: str
    sub_city: str
    building_name: str
    id: int = None

    @classmethod
    def from_instance(cls, camera_model: "Camera") -> "CameraDataClass":
        return cls(
            id = camera_model.id,
            active = camera_model.active,
            city = camera_model.city,
            sub_city = camera_model.sub_city,
            building_name = camera_model.building_name
        )
    

@dataclasses.dataclass
class AlertDataClass:
    camera: CameraDataClass = None
    target: target_services.TargetDataClass = None
    facePicLocation: str = None
    rec_time: datetime.datetime = None
    id: int = None

    @classmethod
    def from_instance(cls, alert_model: "Alert") -> "AlertDataClass":
        return cls(
            id = alert_model.id,
            camera = alert_model.camera,
            target = alert_model.target,
            facePicLocation = alert_model.facePicLocation,
            rec_time = alert_model.rec_time
        )
    

def register_camera(data: "CameraDataClass") -> "CameraDataClass":
    camera_create = fr_models.Camera.objects.create(
        active = data.active,
        city = data.city,
        sub_city = data.sub_city,
        building_name = data.building_name
    )
    return CameraDataClass.from_instance(camera_model=camera_create)

def get_cameras() -> list["CameraDataClass"]:
    camera = fr_models.Camera.objects.filter()

    return [
        CameraDataClass.from_instance(single_camera) for single_camera in camera
    ]


def update_camera(camera_id: int, camera_data: "CameraDataClass"):
    camera = get_object_or_404(fr_models.Camera, pk=camera_id)

    camera.active = camera_data.active
    camera.save()

    return CameraDataClass.from_instance(camera_model=camera)

def get_camera(camera_id) -> "CameraDataClass":
    camera = get_object_or_404(fr_models.Camera, pk=camera_id)
    return CameraDataClass.from_instance(camera_model=camera)

def get_alerts() -> list["AlertDataClass"]:
    alert = fr_models.Alert.objects.filter()

    return [
        AlertDataClass.from_instance(single_alert) for single_alert in alert
    ]

def get_target_alert(target_id) -> "AlertDataClass":
    target = target_models.Target.objects.get(pk=target_id)
    alerts = fr_models.Alert.objects.filter(target=target)

    return [
        AlertDataClass.from_instance(single_alert) for single_alert in alerts
    ]


def register_alert(data) -> "AlertDataClass":
    camObj = fr_models.Camera.objects.get(pk=int(data["camera"]))
    tarObj = target_models.Target.objects.get(pk=int(data["target"]))
    
    alert_create = fr_models.Alert.objects.create( 
        camera = camObj,
        target = tarObj,
        facePicLocation = data["facePicLocation"],
        rec_time = data["rec_time"]
    )
    return AlertDataClass.from_instance(alert_model=alert_create)
