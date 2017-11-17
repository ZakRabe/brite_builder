# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Loadout(models.Model):
    build_hash  = models.CharField(max_length=32)
    talent_0    = models.ForeignKey('talents.Talent', related_name="+")
    talent_1    = models.ForeignKey('talents.Talent', related_name="+")
    talent_2    = models.ForeignKey('talents.Talent', related_name="+")
    talent_3    = models.ForeignKey('talents.Talent', related_name="+")
    talent_4    = models.ForeignKey('talents.Talent', related_name="+")
    
class Build(models.Model):
    title       = models.CharField(max_length=150)
    description = models.CharField(max_length=500)    
    loadout     = models.ForeignKey('Loadout')