# Generated by Django 4.2.1 on 2023-05-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='facePicLocation',
            field=models.ImageField(default='AlertPic/None/No0img.jpg', max_length=255, upload_to='AlertPic/', verbose_name='Face Image'),
        ),
    ]
