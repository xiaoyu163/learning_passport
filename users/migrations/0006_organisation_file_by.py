# Generated by Django 4.1.3 on 2023-06-17 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_organisation_file_organisation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='file_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
    ]
