# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from champs.models import Champ
from talents.models import Talent, SpecialTalent
from .templatetags.html_filters import champName
from builds.models import Loadout, Build, Favorite
from builds.common import create_loadout
from news.models import News
from site_auth.models import Profile

# Create your views here.
def index(request, champ_name, loadout=None, build_id=None):
    champs = Champ.objects.all().exclude(title="Shared");
    selected_champ = None

    if champ_name is not None:
        selected_champ = get_object_or_404(Champ, title__iexact=champName(champ_name))
        news = None
    else:
        news = [news for news in News.objects.all().order_by('-id')[0:5]]
    if build_id is not None:
        build = Build.objects.filter(id=build_id)
        if build.exists():
            # loadout = json.dumps(build[0].loadout.to_json())
            build = json.dumps(build[0].to_json(request))
    else:
        build = json.dumps(None)


    return render(request, 'site/index.html', {'champs': champs, 'selected_champ':selected_champ, 'loadout': loadout, "build":build, "news":news})

def profile(request, username=None):
    champs = Champ.objects.all().exclude(title="Shared");

    if username is None:
        # show my own profile on /profile/
        if request.user.is_authenticated():
            # temporary until us 3 have profiles
            if request.user.profile is None:
                profile = Profile(user_id=request.user.id)
                profile.save()
            # /temp
            my_builds = Build.objects.select_related('user').filter(user_id=request.user.id)
            favs = Favorite.objects.select_related('build').filter(user_id=request.user.id)
            builds = [my_build for my_build in my_builds] + [fav.build for fav in favs]
            target_user = None
        else:
            return redirect('/')
    else:
        target_user = get_object_or_404(User, username__iexact=username)
        builds = Build.objects.select_related('user').filter(user_id=target_user.id)



    return render(request, 'site/profile.html', {'champs': champs, 'builds': builds, 'target_user': target_user})

def build(request,champ_name,loadout,build_id=None):

    build_hash_data = "[" + loadout + "]"
    # return HttpResponse(build_hash_data)
    build_hash = json.dumps(sorted(json.loads(build_hash_data)))

    loadout = Loadout.objects.filter(build_hash=build_hash)

    if loadout.exists() is False:
        return index(request, champ_name, build_hash_data)

    if build_id is None:
        return index(request, champ_name, json.dumps(loadout[0].to_json(request)))
    else:
        return index(request, champ_name, json.dumps(loadout[0].to_json(request)), build_id)
