# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 05:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0003_auto_20171120_0450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='build',
            old_name='user_id',
            new_name='user',
        ),
    ]
