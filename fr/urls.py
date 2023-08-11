from django.urls import path

from . import apis

urlpatterns = [
    path("camera/", apis.CameraCreateApi.as_view(), name="camera"),
    path(
        "camera/<int:camera_id>/",
        apis.CameraStatusUpdateApi.as_view(),
        name="camera_status",
    ),
    path("alert/", apis.AlertCreateAPi.as_view(), name="alert"),
    path(
        "alert/<int:target_id>/",
        apis.TargetAlertAPI.as_view(),
        name="target_alerts",
    ),
]