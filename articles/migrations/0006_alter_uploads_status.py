# Generated by Django 4.1.3 on 2023-06-16 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_uploads_remove_article_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploads',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]