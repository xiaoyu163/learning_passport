# Generated by Django 4.1.3 on 2023-10-27 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0018_alter_article_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='year',
            new_name='date',
        ),
    ]
