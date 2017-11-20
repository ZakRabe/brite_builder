# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response, get_object_or_404, render
from brite_builder.templatetags.html_filters import champName
from django.http import HttpResponse, JsonResponse
from .models import Talent, TalentType,SpecialTalent
from champs.models import Champ

# Create your views here.
def css(request):
    types = TalentType.objects.all()
    return render_to_response('talents/styles.css', context={'types': types}, content_type="text/css")

def doRender(request,id):
    return render(request, 'site/_talent.html')

def champTalentPool(request, title):
    selected_champ = get_object_or_404(Champ, title__iexact=champName(title))
    talents = Talent.objects.select_related('spell__champ').filter(spell__champ_id=selected_champ.id).order_by('spell__button', 'no_limit', 'type_id')
    special_talents = SpecialTalent.objects.select_related('talent__spell__champ').filter(champ_id=selected_champ.id)
    talents = [talent.to_json() for talent in talents] + [special_talent.talent.to_json() for special_talent in special_talents]
    return JsonResponse(talents, safe=False);

