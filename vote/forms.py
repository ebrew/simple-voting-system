from django import forms
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class LoginForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = User
        fields = ['username']


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=20, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=20, required=True)
    image = forms.ImageField(required=False, help_text='Required for the contestants')
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False,
                                      help_text='Required for the contestants')

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'image', 'position')

