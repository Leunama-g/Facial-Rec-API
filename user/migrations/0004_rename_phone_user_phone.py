# Generated by Django 4.2.1 on 2023-05-23 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_phone_user_clearance_lvl_user_middle_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Phone',
            new_name='phone',
        ),
    ]
