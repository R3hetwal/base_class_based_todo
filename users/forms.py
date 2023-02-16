from django import forms
from django.forms import ModelForm
from users.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 

class SignupForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User

class EditUserProfileForm(UserChangeForm):
    # password = None 
    # class Meta:
    #     model = User
    #     fields = ['email', 'username', 'first_name', 'last_name', 'start_date', 'last_login']
    #     labels = {'email': 'Email'}


    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}))
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'start_date', 'last_login', 'current_password']
    