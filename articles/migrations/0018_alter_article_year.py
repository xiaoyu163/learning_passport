# Generated by Django 4.1.3 on 2023-10-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_article_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='year',
            field=models.DateField(),
        ),
    ]