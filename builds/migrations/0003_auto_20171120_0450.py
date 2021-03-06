# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 04:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builds', '0002_build'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loadout',
            name='build_hash',
            field=models.CharField(max_length=200),
        ),
    ]
