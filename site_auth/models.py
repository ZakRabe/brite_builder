# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

NONE = 'Unknown'
US_E = "US East"
US_SE = "US South-East"
US_SW = "US South-West"
US_W = "US West"
SPAIN = "Spain"
EU_E = "EU East"
POL = "Poland"
EU_N = "EU North"
PERU = "Peru"
CHILE = "Chile"
SA = "South America"
JP = "Japan"
IND = "India"
IND_E = "India East"
AUS = "Australia"
HK = "Hong Kong"
ARF_S = "South Africa"
ASIA = "Asia"


SERVER_CHOICES = (
    (0,NONE),
    (1,US_E),
    (2,US_SE),
    (3,US_SW),
    (4,US_W),
    (5,SPAIN),
    (6,EU_E),
    (7,POL),
    (8,EU_N),
    (9,PERU),
    (10,CHILE),
    (11,SA),
    (12,JP),
    (13,IND),
    (14,IND_E),
    (15,AUS),
    (16,HK),
    (17,ARF_S),
    (18,ASIA),
)


# Create your models here.
class Profile(models.Model):
    avatar_url= models.CharField(max_length=150)
    subtitle= models.CharField(max_length=32)
    server= models.IntegerField(choices=SERVER_CHOICES, default=0)
    # in game name
    ign =models.CharField(max_length=64)