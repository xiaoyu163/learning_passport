# Generated by Django 4.1.3 on 2023-11-28 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_student_cd_date_student_pd_date_student_rm_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cd_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='pd_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='rm_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='viva_status',
            field=models.BooleanField(default=False),
        ),
    ]
