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
from .common import create_loadout


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
        returned = create_loadout(data, self.request)
        if returned.get('errors', None) is not None:
            return returned
        else:
            loadout = returned.get('loadout')
            clean = returned.get('clean')

        build_dict = {
            'title' : clean.get('title'),
            'description' : clean.get('description'),
        }
        del clean['title']
        del clean['description']
        # create new build
        if self.request.user.is_authenticated():
            return True
            build_dict['user_id'] = self.request.user.id
            # check if the user already has a build with this loadout,
            # if so, update instead of create
        build_dict['loadout_id'] = loadout.id

        build = Build(**build_dict)
        build.save()
        # messages.success(self.request,"Build Saved!")
        struct = {
            'build': build.to_json(),
            'loadout': build.to_json()['loadout'],
        }
        return {"success": struct}


    def wrap(self,request):
        self.request = request
        return JsonResponse(self.save(), safe=False)