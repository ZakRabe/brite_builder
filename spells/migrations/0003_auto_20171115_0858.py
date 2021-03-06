# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 08:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spells', '0002_auto_20171115_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spell',
            name='button',
            field=models.IntegerField(blank=True, choices=[(0, 'LMB'), (1, 'RMB'), (2, 'Space'), (3, 'Q'), (4, 'E'), (5, 'R'), (6, 'F')], null=True),
        ),
        migrations.AlterField(
            model_name='spell',
            name='champ',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='champs.Champ'),
        ),
    ]
