# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from champs.models import Champ
from talents.models import Talent, SpecialTalent
from .templatetags.html_filters import champName

# Create your views here.
def index(request, champ_name):
    champs = Champ.objects.all()
    selected_champ = None

    if champ_name is not None:
        selected_champ = get_object_or_404(Champ, title__iexact=champName(champ_name))
    return render(request, 'site/index.html', {'champs': champs, 'selected_champ':selected_champ})

def profile(request):
    champs = Champ.objects.all()
    return render(request, 'site/profile.html', {'champs': champs})