# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0004_auto_20171120_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
