# Generated by Django 4.1.2 on 2022-10-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0010_alter_company_profile_cimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_profile',
            name='cdescription',
            field=models.CharField(max_length=5000),
        ),
    ]
