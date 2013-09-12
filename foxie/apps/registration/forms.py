from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username",)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = TextInput(attrs={'placeholder':'First Name',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['last_name'].widget = TextInput(attrs={'placeholder':'Last Name',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['email'].widget = TextInput(attrs={'placeholder':'Email Address',
                                                          'class':'form-control',
                                                          'type':'email',
                                                          'required':''})
        self.fields['username'].widget = TextInput(attrs={'placeholder':'Username',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder':'Password',
                                                          'class':'form-control',
                                                          'required':''})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder':'Confirm Password',
                                                          'class':'form-control',
                                                          'required':''})
