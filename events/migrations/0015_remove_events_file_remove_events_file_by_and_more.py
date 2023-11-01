# Generated by Django 4.1.3 on 2023-09-21 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0009_orgcomittee'),
        ('events', '0014_alter_announcement_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='file',
        ),
        migrations.RemoveField(
            model_name='events',
            name='file_by',
        ),
        migrations.RemoveField(
            model_name='events',
            name='status',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comittee',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AlterField(
            model_name='comittee',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.organisation'),
        ),
        migrations.AlterField(
            model_name='comittee',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AlterField(
            model_name='event_participants',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.events'),
        ),
        migrations.AlterField(
            model_name='event_participants',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AlterField(
            model_name='othercomp',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.CreateModel(
            name='Event_Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(null=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.events')),
                ('submit_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.student')),
            ],
        ),
        migrations.AddField(
            model_name='event_participants',
            name='event_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.event_form'),
        ),
    ]
