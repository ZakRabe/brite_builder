# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from brite_builder.common import get_post_json
from champs.models import Champ
from django.contrib import messages
from brite_builder.templatetags.html_filters import champName
from .models import Loadout
from .models import Build
from .forms import BuildForm


# Create your views here.
def router(request):
    if request.method == "POST":
        return RestCreate().wrap(request)
    if request.method == "GET":
        return RestRead().wrap(request)

class RestRead():

    def find(self):
        return self.request.GET

    def wrap(self,request):
        self.request = request
        return JsonResponse(self.find())

class RestCreate():

    def save(self):
        data = get_post_json(self.request)

        for attr in ['talent_0','talent_1','talent_2','talent_3', 'talent_4']:
            if data[attr] is not None:
                data[attr+"_id"] = data[attr]['id']

        referer = self.request.META.get('HTTP_REFERER')
        champ_name = referer.split('/')[3]
        champ = get_object_or_404(Champ,title__iexact=champName(champ_name))
        data['champ_name'] = champ_name
        build_data = data.get('build', {});
        data['title'] = build_data.get('title', "Unnamed Loadout")
        data['description'] = build_data.get('description', "")

        form = BuildForm(data)


        if not form.is_valid():
            return {"errors":form.errors}

        clean = form.cleaned_data

        build_dict = {

            'title' : clean.get('title'),
            'description' : clean.get('description'),

        }
        del clean['title']
        del clean['description']
        if clean.get('id', None) is None:
            # look up if there's an existing loadout for this build_hash
            loadout = Loadout.objects.filter(build_hash=clean.get('build_hash'))
            if loadout.count() == 0:
                # strip our validation values
                del clean['champ_name']
                # create new loadout for the build
                loadout = Loadout(**clean)
                loadout.save()
            else:
                loadout = loadout[0]

        if self.request.user.is_authenticated():
            # create new build
            build_dict['user_id'] = self.request.user.id
            build_dict['loadout_id'] = loadout.id

            build = Build(**build_dict)
            build.save()
            return {"success": build.to_json()}
        # messages.success(self.request,"Build Saved!")
        return {'success':loadout.to_json()}

    def wrap(self,request):
        self.request = request
        return JsonResponse(self.save(), safe=False)