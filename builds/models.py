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
    
    def to_json(self):
        return {
            "build_hash": self.build_hash,
            "talent_0": self.talent_0.to_json(),
            "talent_1": self.talent_1.to_json(),
            "talent_2": self.talent_2.to_json(),
            "talent_3": self.talent_3.to_json(),
            "talent_4": self.talent_4.to_json(),
        }
    
class Build(models.Model):
    title       = models.CharField(max_length=150)
    description = models.CharField(max_length=500)    
    loadout     = models.ForeignKey('Loadout')
    
    def to_json(self):
        return {
            "title":self.title,
            "description":self.description,
            "loadout":self.loadout.to_json(),
        }