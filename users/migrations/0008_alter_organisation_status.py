# Generated by Django 4.1.3 on 2023-06-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_organisation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='status',
            field=models.BooleanField(null=True),
        ),
    ]
