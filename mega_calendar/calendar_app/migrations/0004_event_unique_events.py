# Generated by Django 4.0.3 on 2022-04-09 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0003_alter_event_country'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('title', 'start_time', 'end_time'), name='unique_events'),
        ),
    ]
