# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 19:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0002_champ_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='champ',
            options={'ordering': ['type']},
        ),
    ]
