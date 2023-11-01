# Generated by Django 4.1.3 on 2023-10-11 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_event_participants_external_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'Seminar/Talk'), (2, 'Conference'), (3, 'Proposal Defense'), (4, 'Candidatual Defense'), (5, 'Welcome Week/Month'), (6, 'Chinese Studies Night'), (7, 'Workshop'), (8, 'Others')], null=True),
        ),
    ]
