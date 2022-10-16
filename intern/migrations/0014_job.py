# Generated by Django 4.1.2 on 2022-10-16 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intern', '0013_newsletters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_position', models.CharField(max_length=100)),
                ('salary', models.IntegerField()),
                ('job_description', models.CharField(max_length=1000)),
                ('job_experience', models.CharField(default='Fresher', max_length=100)),
                ('cname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intern.company_profile')),
            ],
        ),
    ]
