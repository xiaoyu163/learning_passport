# Generated by Django 4.1.3 on 2023-09-09 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_events_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='poster',
            field=models.FileField(default=0, upload_to='event_poster/'),
            preserve_default=False,
        ),
    ]
