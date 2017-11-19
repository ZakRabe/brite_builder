# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from champs.models import Champ
from .forms import RegisterForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated():
        return redirect('/')
    champs = Champ.objects.all().exclude(title="Shared");
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth/login.html', {"error": "Unable to login with this Username and Password","champs":champs})
    else:
        return render(request, 'auth/login.html', {"champs":champs})
    
        
def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    champs = Champ.objects.all().exclude(title="Shared");
    if request.method == "POST":
        form = RegisterForm(request.POST)    
        if form.is_valid() is False:
          return render(request, 'auth/register.html', {'form': form, "champs":champs})
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        return render(request, 'auth/register.html', {"form": form, "champs":champs})
    else:
        form = RegisterForm()   
        return render(request, 'auth/register.html',  {'form':form,"champs":champs})