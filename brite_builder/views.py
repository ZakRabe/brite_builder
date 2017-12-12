# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import json
import re
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from champs.models import Champ
from talents.models import Talent, SpecialTalent
from .templatetags.html_filters import champName
from builds.models import Loadout, Build, Favorite
from builds.common import create_loadout
from news.models import News
from site_auth.models import Profile
from site_auth.forms import ProfileEditForm

# Create your views here.
def index(request, champ_name, loadout=None, build_id=None):
    champs = Champ.objects.filter(active=1).exclude(title="Shared");
    selected_champ = None

    if champ_name is not None:
        selected_champ = get_object_or_404(Champ, title__iexact=champName(champ_name))
        news = None
    else:
        news = [news for news in News.objects.all().order_by('-id')[0:5]]
    if build_id is not None:
        build = Build.objects.filter(id=build_id)
        if build.exists():
            build_model = build[0]
            # loadout = json.dumps(build[0].loadout.to_json())
            if not request.user.is_authenticated() or request.user.id != build_model.user.id:
                build_model.view_count = build_model.view_count + 1
                build_model.save()

            build = json.dumps(build_model.to_json(request))
    else:
        build = json.dumps(None)


    return render(request, 'site/index.html', {'champs': champs, 'selected_champ':selected_champ, 'loadout': loadout, "build":build, "news":news})

def profile(request, username=None):
    champs = Champ.objects.filter(active=1).exclude(title="Shared");

    if username is None:
        # show my own profile on /profile/
        if request.user.is_authenticated() == True:


            if request.method == "POST":
                profile_form = ProfileEditForm(request.POST)
                if profile_form.is_valid():
                    messages.success(request,"Profile Updated!")
                    request.user.profile.update(**profile_form.cleaned_data)
            else:
                profile_form = ProfileEditForm(request.user.profile.to_json())
            favs = Favorite.objects.select_related('build').filter(user_id=request.user.id).order_by('build_id')
            favs = [fav.build.id for fav in favs]
            my_builds = Build.objects.select_related('user').filter(Q(user_id=request.user.id)| Q(id__in=favs)).order_by('-id')
            builds = [my_build for my_build in my_builds]
            target_user = None
        else:
            return redirect('/')
    else:
        profile_form = None
        target_user = get_object_or_404(User, username__iexact=username)
        favs = Favorite.objects.select_related('build').filter(user_id=target_user.id).order_by('build_id')
        favs = [fav.build.id for fav in favs]
        builds = Build.objects.select_related('user').filter(Q(user_id=target_user.id)| Q(id__in=favs)).order_by('-id')



    return render(request, 'site/profile.html', {'profile_edit_form':profile_form,'champs': champs, 'builds': builds, 'target_user': target_user})

def build(request,champ_name,loadout,build_id=None):
    cleaned = re.sub('-',',', loadout)
    build_hash_data = "[" + cleaned + "]"
    # return HttpResponse(build_hash_data)
    build_hash = json.dumps(sorted(json.loads(build_hash_data)))

    loadout = Loadout.objects.filter(build_hash=build_hash)

    if loadout.exists() is False:
        return index(request, champ_name, build_hash_data)

    if build_id is None:
        return index(request, champ_name, json.dumps(loadout[0].to_json(request)))
    else:
        return index(request, champ_name, json.dumps(loadout[0].to_json(request)), build_id)