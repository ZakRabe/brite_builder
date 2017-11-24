from django import forms
import re
import sys
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.contrib.auth.models import User
from urlparse import urlparse
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

class ProfileEditForm(forms.Form):
    subtitle    = forms.CharField(max_length=32, required=False)
    avatar_url  = forms.CharField(max_length=150, required=False)
    ign         = forms.CharField(max_length=64, required=False)

    def clean_avatar_url(self):
        url = self.cleaned_data['avatar_url']
        obj = urlparse(url)
        scheme = obj.scheme
        # if scheme is none, the host will be in path instead
        if scheme == '':
            host = obj.path
            try:
                path_index = host.index('/')
                path = host[path_index:]
            except ValueError, e:
                path = ''
                self._errors['avatar_url'] = ["what are you doing?"]
        else:
            host = obj.netloc
            path = obj.path
        if path == '' or path is None:
            self._errors['avatar_url'] = ["what are you doing?"]

        allowed_hosts = ['i.imgur.com', 'www.i.imgur.com', ]
        if host not in allowed_hosts:
            self._errors['avatar_url'] = ["Upload to imgur, right click -> Copy image address"]
        new_url = 'https://' + host + path
        prog = re.compile('https://\S+?\.(?:jpg|jpeg|png)')
        result = prog.match(new_url)
        if result is None:
            self._errors['avatar_url'] = ["Invalid image type, use JPG or PNG please"]
        return new_url