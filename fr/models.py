from django.db import models
from target.models import Target

class Camera(models.Model):
    city = models.CharField(verbose_name="City", max_length=255)
    sub_city = models.CharField(verbose_name="Sub City", max_length=255)
    building_name = models.CharField(verbose_name="Building Name", max_length=255)
    active = models.BooleanField(verbose_name="Active")

class Alert(models.Model):
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        verbose_name="Target"
    )
    camera = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        verbose_name="Camera"
    )
    rec_time = models.DateTimeField(verbose_name="REC TIME",  max_length=255)
    facePicLocation = models.ImageField(verbose_name="Face Image",upload_to="AlertPic/",default="AlertPic/None/No0img.jpg", max_length=255)
    

