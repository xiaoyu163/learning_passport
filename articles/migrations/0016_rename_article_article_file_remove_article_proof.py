# Generated by Django 4.1.3 on 2023-10-11 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_remove_article_art_front_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article',
            new_name='file',
        ),
        migrations.RemoveField(
            model_name='article',
            name='proof',
        ),
    ]