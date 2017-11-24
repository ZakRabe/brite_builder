# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from site_auth.common import user_to_json
import platform


# Create your models here.
class Loadout(models.Model):
    build_hash  = models.CharField(max_length=200)
    talent_0    = models.ForeignKey('talents.Talent', related_name="+")
    talent_1    = models.ForeignKey('talents.Talent', related_name="+")
    talent_2    = models.ForeignKey('talents.Talent', related_name="+")
    talent_3    = models.ForeignKey('talents.Talent', related_name="+")
    talent_4    = models.ForeignKey('talents.Talent', related_name="+")

    @property
    def all(self):
        talents = []
        if self.talent_0 is not None:
            talents.append(self.talent_0)
        if self.talent_1 is not None:
            talents.append(self.talent_1)
        if self.talent_2 is not None:
            talents.append(self.talent_2)
        if self.talent_3 is not None:
            talents.append(self.talent_3)
        if self.talent_4 is not None:
            talents.append(self.talent_4)
        return talents

    @property
    def champ(self):
        talents = self.all
        for talent in talents:
            if talent is not None:
                return talent.spell.champ.title

    @property
    def champ_type(self):
        talents = self.all
        for talent in talents:
            if talent is not None:
                return talent.spell.champ.c_type

    def favorited(self, request):
        return self.favorites.filter(user_id=request.user.id).count() > 0

    def to_json(self, request):
        return {
            "id": self.id,
            "build_hash": self.build_hash,
            "talent_0": self.talent_0.to_json(),
            "talent_1": self.talent_1.to_json(),
            "talent_2": self.talent_2.to_json(),
            "talent_3": self.talent_3.to_json(),
            "talent_4": self.talent_4.to_json(),
            "favorited": self.favorited(request)
        }

class Build(models.Model):
    title       = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    user        = models.ForeignKey('auth.User', null=True)
    loadout     = models.ForeignKey('Loadout')

    @property
    def url(self):
        talents = self.loadout.all
        build_hash = self.loadout.build_hash.replace(' ','').replace("[",'').replace(']', '')
        return "/" + self.loadout.talent_0.champ_link + "/"+ build_hash + "/" + str(self.id)

    @property
    def champ(self):
        return self.loadout.champ

    def favorited(self, request):
        return self.favorites.filter(user_id=request.user.id).count() > 0


    def to_json(self, request):
        return {
            "id" : self.id,
            "title":self.title,
            "description":self.description,
            "loadout":self.loadout.to_json(request),
            'user': user_to_json(self.user) if self.user is not None else None,
            "favorited": self.favorited(request)
        }


class BuildSet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    builds = models.ManyToManyField(Build)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user    = models.ForeignKey('auth.User', related_name="favorites")
    build   = models.ForeignKey('Build', null=True, related_name="favorites", on_delete=models.CASCADE)
    loadout = models.ForeignKey('Loadout', null=True, related_name="favorites")