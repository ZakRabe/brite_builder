# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import time

# Create your models here.
class News(models.Model):
    title   = models.CharField(max_length=100)
    html    = models.TextField(max_length=1000, default="")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title