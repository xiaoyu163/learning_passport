# Generated by Django 4.1.3 on 2023-09-20 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_organisation_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgComittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.organisation')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student')),
            ],
        ),
    ]