# Generated by Django 4.1.3 on 2023-11-06 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_alter_article_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='apa',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
