# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0002_auto_20171115_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='talent',
            name='is_global',
            field=models.BooleanField(default=False),
        ),
    ]