from django import forms
import re
import sys
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    captcha =  ReCaptchaField(widget=ReCaptchaWidget())
    email   = forms.CharField(required=True)


    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if exists:
            self._errors['email'] = ["Email address is already registered"]
        return email
