# Generated by Django 4.1.3 on 2023-10-24 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_rename_lecturer_lecturer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='lecturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.lecturer'),
            preserve_default=False,
        ),
    ]