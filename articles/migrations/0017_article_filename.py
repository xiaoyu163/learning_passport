# Generated by Django 4.1.3 on 2023-10-15 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_rename_article_article_file_remove_article_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='filename',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
