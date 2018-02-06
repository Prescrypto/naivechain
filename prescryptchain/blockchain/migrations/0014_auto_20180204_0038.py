# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-04 06:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blockchain', '0013_auto_20170726_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='rxid',
            field=models.CharField(blank=True, default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='block',
            name='poetxid',
            field=models.CharField(blank=True, default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='private_key',
            field=models.CharField(blank=True, default=b'', max_length=3000),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='public_key',
            field=models.CharField(blank=True, default=b'', max_length=3000),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 2, 4, 6, 38, 45, 505945, tzinfo=utc)),
        ),
    ]
