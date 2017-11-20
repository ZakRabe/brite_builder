# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from champs.models import Champ
from talents.models import Talent, SpecialTalent
from .templatetags.html_filters import champName
from builds.models import Loadout
from builds.common import create_loadout

# Create your views here.
def index(request, champ_name, loadout=None, build_id=None):
    champs = Champ.objects.all().exclude(title="Shared");
    selected_champ = None

    if champ_name is not None:
        selected_champ = get_object_or_404(Champ, title__iexact=champName(champ_name))
    return render(request, 'site/index.html', {'champs': champs, 'selected_champ':selected_champ, 'loadout': loadout})

def profile(request):
    champs = Champ.objects.all().exclude(title="Shared");
    return render(request, 'site/profile.html', {'champs': champs})

def build(request,champ_name,loadout,build_id=None):

    build_hash_data = "[" + loadout + "]"
    build_hash = json.dumps(json.loads(build_hash_data))

    loadout = Loadout.objects.filter(build_hash=build_hash)

    if loadout.exists() is False:
        return index(request, champ_name, build_hash_data)


    if build_id is None:
        return index(request, champ_name, json.dumps(loadout[0].to_json()))
    else:
        return index(request, champ_name, json.dumps(loadout[0].to_json()), build_id)
