# Generated by Django 4.1.3 on 2023-06-25 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_alter_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.BooleanField(),
        ),
    ]