from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=12)
    password2 = forms.CharField(label='Confirm Password (again)' ,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','phone_number']
        labels = {'email':'Email'}