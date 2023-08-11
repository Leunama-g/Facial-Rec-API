from rest_framework import serializers

from . import services

from target import serializer as target_serializer

class CameraSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    active = serializers.BooleanField()  
    city = serializers.CharField()
    sub_city = serializers.CharField()
    building_name = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.CameraDataClass(**data)
    
class AlertSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    camera = CameraSerializer(read_only=True)
    target = target_serializer.TargetSerializer(read_only=True)
    facePicLocation = serializers.ImageField(use_url=True, max_length=None)
    rec_time = serializers.DateTimeField(format="iso-8601", input_formats=["iso-8601"])

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.AlertDataClass(**data)