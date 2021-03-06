# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from champs.models import Champ
from .forms import RegisterForm
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.
def login_view(request):
    if request.user.is_authenticated():
        messages.error(request, "Already logged in")
        return redirect('/')
    champs = Champ.objects.filter(active=1).exclude(title="Shared");
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('/')
        else:
            return render(request, 'auth/login.html', {"error": "Unable to login with this Username and Password","champs":champs})
    else:
        return render(request, 'auth/login.html', {"champs":champs})

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def register(request):
    if request.user.is_authenticated:
        messages.error(request, "Already logged in")
        return redirect('/')
    champs = Champ.objects.filter(active=1).exclude(title="Shared");
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.email = form.cleaned_data['email']
            user.save()
            profile = Profile(user_id=user.id)
            profile.save()
            messages.success(request, "You're signed up, you may now login")
            return redirect('/auth/login')
        return render(request, 'auth/register.html', {'form': form, "champs":champs})
    else:
        form = RegisterForm()
        return render(request, 'auth/register.html',  {'form':form,"champs":champs})