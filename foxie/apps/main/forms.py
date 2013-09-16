from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.widgets import TextInput, PasswordInput, Textarea
from django.contrib.auth.models import User
from django import forms

from foxie.apps.main.models import Yip, Follower

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username',
                                                          'class': 'form-control',
                                                          'required':''})
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password',
                                                          'class': 'form-control',
                                                          'required':''})

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)

class YipForm(forms.ModelForm):
    class Meta:
        model = Yip
        exclude = ('user','dt','tags',)

class FollowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FollowForm, self).__init__(*args, **kwargs)
        self.fields['followee'].to_field_name="username"
        self.fields['followee'].widget = TextInput(attrs={'placeholder': 'Find Someone',
                                                          'class': 'form-control',
                                                          'required':''})
 
    class Meta:
        model = Follower
        exclude = ('follower',)

class ContactForm(forms.Form):
    sender  = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=Textarea(attrs={'resize':'none'}))
