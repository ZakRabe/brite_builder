# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from brite_builder.common import get_post_json
from champs.models import Champ
from django.contrib import messages
from brite_builder.templatetags.html_filters import champName
from .models import Loadout, Build, Favorite
from .forms import BuildForm
from .common import create_loadout


# Create your views here.
def router(request, build_id=None):
    if request.method == "POST":
        return RestCreate().wrap(request)
    if request.method == "DELETE":
        return RestDelete().wrap(request, build_id)
    # if request.method == "GET":
    #     return RestRead().wrap(request)

class RestCreate():

    def save(self):
        data = get_post_json(self.request)
        # make sure the user authed owns the build they are editing
        if data.get('build', None) is not None:
            if data['build'].get('id', None) is not None:
                if self.request.user.is_authenticated():
                    build = get_object_or_404(Build, id=data['build']['id'])
                    if self.request.user.id != build.user.id:
                        return {'error': "403"}
                else:
                    return {'error': "403"}
        returned = create_loadout(data, self.request)
        if returned.get('errors', None) is not None:
            return returned
        else:
            loadout = returned.get('loadout')
            # print >>sys.stderr, loadout.to_json(self.request)['build_hash']
            clean = returned.get('clean')
        build_dict = {
            'title' : clean.get('title'),
            'description' : clean.get('description'),
            'id' : clean.get('id'),
        }
        del clean['title']
        del clean['description']
        # create new build
        if self.request.user.is_authenticated():
            build_dict['user_id'] = self.request.user.id
            # check if the user already has a build with this loadout,
            # if so, update instead of create
        build_dict['loadout_id'] = loadout.id

        build = Build(**build_dict)
        build.save()
        # messages.success(self.request,"Build Saved!")
        struct = {
            'build': build.to_json(self.request),
            'loadout': build.to_json(self.request)['loadout'],
        }
        return {"success": struct}
    def wrap(self,request):
        self.request = request

        return JsonResponse(self.save(), safe=False)

class RestDelete():

    def delete(self, build_id):
        if self.request.user.is_authenticated() == False:
            return {'error': "403"}
        build = get_object_or_404(Build, id=build_id)
        if self.request.user.id != build.user.id:
            return {'error': "403"}
        build.delete()
        return {"success": "OK"}


    def wrap(self,request, build_id):
        self.request = request

        return JsonResponse(self.delete(build_id), safe=False)

def delete_favorite(request, build_id, queryset):
    delete_build = request.POST.get('target') == 'build'
    response = None
    if delete_build == True:
        if queryset.exists() == False:
            response = {'error': '405'}
        else:
            fav = Favorite.objects.filter(user_id=request.user.id, build_id=build_id)
            if fav.exists() == False:
                response = {'error':'404'}
            else:
                fav.delete()
                response = {'success':'Deleted fav by build'}
    else:
        loadout = Loadout.objects.filter(id=build_id)
        if loadout.exists() == False:
            response = {'error': '405'}
        else:
            fav = Favorite.object.filter(user_id=request.user.id, loadout_id=loadout[0].id)
            if fav.exists() == False:
                response = {'error':'404'}
            else:
                fav.delete()
                response = {'success': 'Deleted fav by loadout'}
    return response
def favorite(request, build_id):
    if request.method == 'POST':
        request.POST = get_post_json(request)
        if request.user.is_authenticated():

            build = Build.objects.filter(id=build_id)
            if request.POST.get('action', None) == 'delete':
                response = delete_favorite(request, build_id, build)
            else:
                # check POST for target type
                if request.POST.get('target') == 'loadout':
                    loadout = Loadout.objects.filter(id=build_id)
                    if loadout.exists() == False:
                        response = {'error': '405'}
                    else:
                        fav = Favorite.object.filter(user_id=request.user.id, loadout_id=loadout[0].id)
                        fav_exists = Favorite.objects.filter(user_id=request.user.id, build_id=build_id).exists()
                        if fav_exists == False:
                            fav = Favorite()
                            fav.build_id = None
                            fav.loadout_id = build[0].loadout.id
                            fav.user = request.user
                            fav.save()
                            # success!
                            response = {'success': 'Favorited by loadout'}
                        else:
                            # user already favorited
                            response = {'error': '422'}
                else:
                    # confirm build exists
                    if build.exists() == True:
                        # check the user hasn't already favorited
                        fav_exists = Favorite.objects.filter(user_id=request.user.id, build_id=build_id).exists()
                        if fav_exists == False:
                            # check if the user is trying to favorite their own build
                            if build[0].user is not None and build[0].user.id == request.user.id:
                                # cant fav ur own shit mate
                                response = {'error':'423'}
                            else:
                                fav = Favorite()
                                fav.build_id = build_id
                                fav.loadout_id = build[0].loadout.id
                                fav.user = request.user
                                fav.save()
                                # success!
                                response = {'success':'Favorited by build'}
                        else:
                            # user already favorited
                            response = {'error': '422'}
                    else:
                        # build not found
                        response = {'error': '405'}
        else:
            # cant fav unless registered/logged in
            response = {'error': 'auth'}
    else:
        # bad method
        response = {'error': '404'}
    return JsonResponse(response, safe=False)

def browser(request):
    champs = Champ.objects.all().exclude(title="Shared")
    return render(request, 'site/browser.html', {'champs':champs})