# Generated by Django 4.1.3 on 2023-06-16 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_organisation_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='file',
        ),
    ]
