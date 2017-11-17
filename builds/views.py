# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse


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
        return self.request.POST
    
    def wrap(self,request):
        self.request = request
        return JsonResponse(self.save())