# Generated by Django 4.0.3 on 2022-04-08 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0002_alter_event_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='country',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='calendar_app.country'),
        ),
    ]
