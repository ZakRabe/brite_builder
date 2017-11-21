# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='html',
            field=models.CharField(default='', max_length=1000),
        ),
    ]