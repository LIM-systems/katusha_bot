# Generated by Django 4.2.5 on 2024-02-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule_app', '5008_alter_abonementjournal_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonements',
            name='time',
            field=models.IntegerField(blank=True, help_text='Указывается в случае если абонемент требует продления', null=True, verbose_name='Время абонемента в месяцах'),
        ),
    ]
