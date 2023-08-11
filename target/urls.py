from django.urls import path

from . import apis

urlpatterns = [
    path("target/", apis.TargetCreateApi.as_view(), name="target"),
    path(
        "target/<int:target_id>/",
        apis.TargetRetrieveUpdate.as_view(),
        name="target_detail",
    ),
]