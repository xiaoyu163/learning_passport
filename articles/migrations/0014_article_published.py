# Generated by Django 4.1.3 on 2023-10-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_remove_article_file_article_art_front_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
