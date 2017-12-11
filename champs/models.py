# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from brite_builder.templatetags.html_filters import champLink

MELEE = "Melee"
RANGED = "Ranged"
SUPPORT   = "Support"

TYPE_CHOICES = (
    (0,MELEE),
    (1,RANGED),
    (2,SUPPORT),
)

# Create your models here.
class Champ(models.Model):
    title       = models.CharField(max_length=50)
    subtitle    = models.CharField(max_length=75)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    c_type      = models.IntegerField(default=1, choices=TYPE_CHOICES)

    class Meta:
        ordering = ['c_type']

    @property
    def image_url(self):
        return "/static/champs/img/icons/" + champLink(self.title) + ".jpg"

    def __str__(self):
        return self.title + ', ' + self.subtitle


    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "c_type": self.c_type,
            "image_url": self.image_url,
            "champ_link": champLink(self.title),
            # "created": self.created,
            # "updated": self.updated,
        }
