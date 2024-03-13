# Generated by Django 4.2.5 on 2024-02-16 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shedule_app', '5007_abonements_abonementjournal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abonementjournal',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата активации'),
        ),
        migrations.AlterField(
            model_name='abonements',
            name='price',
            field=models.IntegerField(verbose_name='Цена рублей'),
        ),
    ]