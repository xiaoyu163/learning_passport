# Generated by Django 4.1.3 on 2023-10-17 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_organisation_filename_orgcomittee_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgcomittee',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.organisation'),
        ),
        migrations.AlterField(
            model_name='orgcomittee',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
    ]
