# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Loadout, Build
# Register your models here.
admin.site.register(Loadout)
admin.site.register(Build)