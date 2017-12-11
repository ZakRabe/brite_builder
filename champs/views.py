# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from .models import Champ

# Create your views here.
def index(request):

    if request.method == "GET":
        champs = Champ.objects.all().exclude(title="Shared")
        champs = [champ.to_json() for champ in champs]
        return JsonResponse(champs, safe=False)