# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 08:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar_url',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ign',
            field=models.CharField(max_length=64, null=True, verbose_name='IGN:'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subtitle',
            field=models.CharField(max_length=32, null=True),
        ),
    ]