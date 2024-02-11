from django import forms
from .models import AccessRequest
from .models import Repository
#from django.contrib.auth.models import User
from django import forms
from .models import Repository, AccessRequest
from django.contrib.auth.forms import UserCreationForm
from . import models
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomAuthenticationForm(AuthenticationForm):
    # Override the labels for the fields
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))  # Use EmailField for email
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
# Import your models

#class AccessRequestForm(forms.ModelForm):
   # user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
  #  repositories= forms.ModelMultipleChoiceField(queryset=Repository.objects.all(), widget=forms.CheckboxSelectMultiple)
  #  access_type = forms.ChoiceField(choices=[('read', 'Read'), ('write', 'Write')])

  #  class Meta:
       # model = AccessRequest
        #fields = ['user', 'repository', 'access_type']
#class AccessRequestForm(forms.ModelForm):
   # user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
   # access_type = forms.ChoiceField(choices=[('read', 'Read'), ('write', 'Write')])

    #def __init__(self, *args, **kwargs):
     #   repo_slug = kwargs.pop('repo_slug', None)
     #   super().__init__(*args, **kwargs)
     #   if repo_slug:
     #       self.fields['repository'].queryset = Repository.objects.filter(repo_slug=repo_slug)

    #class Meta:
     #   model = AccessRequest
     #   fields = ['user', 'repository', 'access_type']


class AccessRequestForm(forms.ModelForm):
    access_type = forms.ChoiceField(choices=[('read', 'Read'), ('write', 'Write')], widget=forms.HiddenInput())

    class Meta:
        model = AccessRequest
        fields = ['access_type']


class RegistrationForm(UserCreationForm):
      # Use 'email' instead of 'Email_address'

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # Use 'email' instead of 'Email_address'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email