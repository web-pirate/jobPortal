# Generated by Django 4.1.2 on 2022-10-26 17:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0005_userdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='user_img',
            field=models.FileField(default=django.utils.timezone.now, upload_to='userProfile'),
            preserve_default=False,
        ),
    ]
