# Generated by Django 4.0.3 on 2022-03-30 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='city',
            new_name='country',
        ),
    ]
