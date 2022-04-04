# Generated by Django 4.0.3 on 2022-04-01 22:13

import calendar_app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0003_alter_country_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='notification',
            field=models.ForeignKey(default=calendar_app.models.Notification.get_default_notification, on_delete=django.db.models.deletion.SET_DEFAULT, to='calendar_app.notification'),
        ),
    ]