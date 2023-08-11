import dataclasses
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from rest_framework import exceptions


import face_recognition
import os
from core import settings
from . import models as Target_models

if TYPE_CHECKING:
    from models import Target


@dataclasses.dataclass
class TargetDataClass:
    first_name: str
    middle_name: str
    last_name: str
    infoDoc: str = None
    facePicLocation: str = None
    last_seen: str = None
    type: str = None
    active: bool = True
    id: int = None

    @classmethod
    def from_instance(cls, Target_model: "Target") -> "TargetDataClass":
        return cls(
            id = Target_model.id,
            first_name = Target_model.first_name,
            last_name = Target_model.last_name,
            middle_name = Target_model.middle_name,
            infoDoc = Target_model.infoDoc,
            facePicLocation = Target_model.facePicLocation,
            last_seen = Target_model.last_seen,
            type = Target_model.type,
            active = Target_model.active
        )

def register_Target(data: "TargetDataClass") -> "TargetDataClass":
    Target_create = Target_models.Target.objects.create(
        first_name = data.first_name,
        last_name = data.last_name,
        middle_name = data.middle_name,
        infoDoc = data.infoDoc,
        facePicLocation = data.facePicLocation,
        last_seen = data.last_seen,
        type = data.type,
        active = data.active,
    )
    return TargetDataClass.from_instance(Target_model=Target_create)

def get_Targets() -> list["TargetDataClass"]:
    Target = Target_models.Target.objects.filter()

    return [
        TargetDataClass.from_instance(single_Target) for single_Target in Target
    ]

def get_target_detail(target_id: int) -> "TargetDataClass":
    target = get_object_or_404(Target_models.Target, pk=target_id)

    return TargetDataClass.from_instance(Target_model=target)

def update_target(target_id: int, target_data: "TargetDataClass", target_ids, face_encodings):
    target = get_object_or_404(Target_models.Target, pk=target_id)

    if target.active != target_data.active:
        if target_data.active == False:
            index = target_ids.index(target_id)
            del target_ids[index]
            del face_encodings[index]

        else:
            media_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'mediafiles')
            pic_loc = media_path + "\\" + str(target.facePicLocation).replace('/', '\\')
            try:
                face_encodings.append(face_recognition.face_encodings(face_image=face_recognition.load_image_file(pic_loc))[0])
                target_ids.append(target_id)
            except IndexError:
                print("face was not encoded")
            else:
                print("face encoded")
        
        print(len(target_ids))

    target.active = target_data.active
    target.first_name = target_data.first_name
    target.middle_name = target_data.middle_name
    target.last_name = target_data.last_name
    target.facePicLocation = target_data.facePicLocation
    target.infoDoc = target_data.infoDoc
    target.last_seen = target_data.last_seen
    target.type = target_data.type
    target.save()

    return TargetDataClass.from_instance(Target_model=target)