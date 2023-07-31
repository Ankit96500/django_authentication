from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

#user signup form
class signupform(UserCreationForm):
    password2=forms.CharField(widget=forms.PasswordInput,label='confirm password(again)')
    class Meta:
        model = User
        fields=['username','email','first_name','last_name']
        labels={'email':'Email'}


#user edit profile form
class usereditprofileform(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields=['username','email','first_name','last_name','date_joined','last_login']
        labels={'email':'Email'}

#user admin profile form
class admineditprofileform(UserChangeForm):
    class Meta:
        model = User
        fields='__all__'
        labels={'email':'Email'}