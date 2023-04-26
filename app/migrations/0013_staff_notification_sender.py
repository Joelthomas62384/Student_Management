# Generated by Django 4.2 on 2023-04-21 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_staff_notification_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_notification',
            name='sender',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
