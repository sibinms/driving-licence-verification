# Generated by Django 3.2.6 on 2022-10-11 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DrivingLicence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_id', models.CharField(blank=True, max_length=250, null=True)),
                ('driving_licence', models.FileField(blank=True, null=True, upload_to='')),
                ('profile', models.FileField(blank=True, null=True, upload_to='')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('issued_by', models.CharField(blank=True, max_length=250, null=True)),
                ('issued_date', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, default='{}', null=True)),
                ('other_details', models.TextField(blank=True, default='{}', null=True)),
                ('authenticity_score', models.FloatField(default=0)),
                ('is_valid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_driving_licence', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]