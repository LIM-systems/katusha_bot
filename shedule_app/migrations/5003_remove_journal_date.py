# Generated by Django 4.2.5 on 2023-11-16 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shedule_app', '5002_journal_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal',
            name='date',
        ),
    ]
