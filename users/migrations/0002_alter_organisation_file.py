# Generated by Django 4.1.3 on 2023-06-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='file',
            field=models.FileField(upload_to='org_com'),
        ),
    ]
