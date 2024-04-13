from django import forms
from django.contrib.auth.models import User
from .models import *

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['skills']
        widgets = {
            'skills': forms.CheckboxSelectMultiple
        }

class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple
        }

class HobbiesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['hobbies']
        widgets = {
            'hobbies': forms.CheckboxSelectMultiple
        }

class CharacterTraitsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['character_traits']
        widgets = {
            'character_traits': forms.CheckboxSelectMultiple
        }

class WantsNeedsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['wants_needs']
        widgets = {
            'wants_needs': forms.CheckboxSelectMultiple
        }

class BackgroundForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background']
        widgets = {
            'background': forms.CheckboxSelectMultiple
        }
