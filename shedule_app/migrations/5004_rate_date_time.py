# Generated by Django 4.2.5 on 2023-11-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule_app', '5003_remove_journal_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время'),
        ),
    ]
