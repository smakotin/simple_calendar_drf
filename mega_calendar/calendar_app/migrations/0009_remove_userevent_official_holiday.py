# Generated by Django 4.0.3 on 2022-04-13 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0008_alter_event_official_holiday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userevent',
            name='official_holiday',
        ),
    ]