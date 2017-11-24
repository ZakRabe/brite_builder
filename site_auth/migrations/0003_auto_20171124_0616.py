# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 06:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_auth', '0002_auto_20171123_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ign',
            field=models.CharField(max_length=64, null=True, verbose_name='IGN'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subtitle',
            field=models.CharField(max_length=32, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
