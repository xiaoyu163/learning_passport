# Generated by Django 4.1.3 on 2023-10-23 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_rename_teacher_lecturer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecturer',
            old_name='lecturer',
            new_name='user',
        ),
    ]
