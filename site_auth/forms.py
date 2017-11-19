from django import forms

from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=32) 
    email = forms.CharField(min_length=3,max_length=100)
    password = forms.CharField(min_length=9)
    confirm = forms.CharField()
    captcha =  ReCaptchaField(widget=ReCaptchaWidget())
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

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