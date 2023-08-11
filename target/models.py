from django.db import models

class Target(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    middle_name = models.CharField(verbose_name="Middle Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    infoDoc = models.ImageField(verbose_name="Document",upload_to="TargetDoc/",default="TargetDoc/None/No0img.jpg", max_length=255)
    facePicLocation = models.ImageField(verbose_name="Face Image",upload_to="TargetPic/",default="TargetPic/None/No0img.jpg", max_length=255)
    last_seen = models.DateTimeField(verbose_name="Last Seen",  max_length=255)
    type = models.CharField(verbose_name="Type", max_length=255)
    active = models.BooleanField(verbose_name="Active")


    
