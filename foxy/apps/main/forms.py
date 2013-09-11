from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput, PasswordInput
from django import forms

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Email',
                                                          'class': 'form-control'})
        self.fields['password'].widget = PasswordInput(attrs={'placeholder': 'Password',
                                                          'class': 'form-control'})
class YipForm(forms.Form):
    text = forms.CharField(max_length=140)
