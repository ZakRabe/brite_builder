from django import forms

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=32) 
    email = forms.CharField(min_length=3,max_length=100)
    password = forms.CharField(min_length=8)
    confirm = forms.CharField(min_length=8)
    captcha =  ReCaptchaField(widget=ReCaptchaWidget())