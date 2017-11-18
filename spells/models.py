# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

LMB = "LMB"
RMB = "RMB"
Q   = "Q"
E   = "E"
SPACE = "Space"
R   = "R"
F   = "F"
SPECIAL   = "Special"

BTN_CHOICES = (
    (0,LMB),
    (1,RMB),
    (2,SPACE),
    (3,Q),
    (4,E),
    (5,R),
    (6,F),
    (7,SPECIAL),
)

# Create your models here.
class Spell(models.Model):
    title   = models.CharField(max_length=50)
    button  = models.IntegerField(choices=BTN_CHOICES, blank=True, null=True)
    champ   = models.ForeignKey('champs.Champ', blank=True, null=True)
    
    def __str__(self):
        if self.champ is not None:
            return self.champ.title + ' - ' + BTN_CHOICES[self.button][1] + ' - ' + self.title
        else:
            return self.title
            
    def to_json(self):
        return {
            'id':self.id,
            'title':self.title,
            'button':BTN_CHOICES[self.button][1],
            'champ':self.champ.to_json(),
        }