# Generated by Django 4.1.3 on 2023-10-16 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_event_participants_filename_events_filename_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_participants',
            name='file',
            field=models.FileField(null=True, upload_to='event_external/'),
        ),
    ]