# Generated by Django 4.1.3 on 2023-10-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_orgcomittee_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgcomittee',
            name='file',
            field=models.FileField(null=True, upload_to='org_external/'),
        ),
    ]