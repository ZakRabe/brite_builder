# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Talent(models.Model):
    title       = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    type        = models.ForeignKey('TalentType')
    spell       = models.ForeignKey('spells.Spell', verbose_name="Spell Image",blank=True, null=True)
    no_limit    = models.BooleanField(verbose_name="Bypass spell count limit", default=False)

    class Meta:
        ordering = ['spell']


    def __str__(self):

        return self.spell.champ.title + " - " + self.title if self.spell is not None and self.spell.champ is not None else self.title

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type.to_json(),
            'spell': self.spell.to_json(),
            "no_limit": self.no_limit,
        }

class TalentType(models.Model):
    title = models.CharField(max_length=15)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.title

    def to_json(self):
        return {
            'id': self.id,
            "title": self.title,
            "color": self.color,
        }

class SpecialTalent(models.Model):
    # these talents will be used for multiple champs
    champ   = models.ForeignKey('champs.Champ')
    talent  = models.ForeignKey('Talent')

    def __str__(self):
        return self.talent.title + " + " + self.champ.title

    def to_json(self):
        return {
            'id': self.id,
            "champ": self.champ.to_json(),
            "talent": self.talent.to_json(),
        }