# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-28 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gfi', '0006_auto_20180228_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securityprices',
            name='change_pct',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='securitypriceshistory',
            name='change_pct',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
