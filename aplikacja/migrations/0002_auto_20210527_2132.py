# Generated by Django 3.1.7 on 2021-05-27 19:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('aplikacja', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 27, 19, 32, 4, 946406, tzinfo=utc), verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='file',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 27, 19, 32, 4, 947091, tzinfo=utc), verbose_name='last modified'),
        ),
    ]
