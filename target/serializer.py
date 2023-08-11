from rest_framework import serializers

from . import services


class TargetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    infoDoc = serializers.ImageField(use_url=True, max_length=None)
    facePicLocation = serializers.ImageField(use_url=True, max_length=None)
    last_seen = serializers.DateTimeField(format="iso-8601", input_formats=["iso-8601"])
    type = serializers.CharField()
    active = serializers.BooleanField()    

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.TargetDataClass(**data)