# Generated by Django 4.1.3 on 2023-10-30 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_alter_event_participants_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='attendance_ontime',
            field=models.BooleanField(null=True),
        ),
    ]
