# Generated by Django 4.1.3 on 2023-10-28 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_rename_year_article_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='file_by',
            new_name='student',
        ),
    ]
