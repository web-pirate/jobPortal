# Generated by Django 4.1.2 on 2022-10-12 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0003_company_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_profile',
            name='cimage',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]