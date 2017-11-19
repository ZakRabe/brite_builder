from django import forms

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=32) 
    email = forms.CharField(min_length=3,max_length=100)
    password = forms.CharField(min_length=8)
    confirm = forms.CharField(min_length=8)
    captcha =  ReCaptchaField(widget=ReCaptchaWidget())
    
    def clean_password(self):
        pw = self.cleaned_data['password']
        
        if len(pw) < 8:
            self._errors["password"] = ["Must have 8 characters"]
        
        return ''
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        exists = User.objects.filter(email=email).exists()
        if exists:
            self._errors["email"] = ["Email already exists in the database"]
    
    def clean_confirm(self):
        form_data = self.cleaned_data
        if form_data["password"] != form_data["confirm"]:
            self._errors["password"] = ["Passwords do not match"]
            self._errors["confirm"] = ["Passwords do not match"]
        return self.cleaned_data['confirm']