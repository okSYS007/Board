

from django.forms import ModelForm 
from django import forms
from .models import Announcement, Files

class InputForm(forms.Form):
      
    login = forms.CharField(max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput())

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['Announcement_title', 'Announcement_text']

class VideoFormEdit(ModelForm):
    class Meta:
        model = Files
        fields = ['File']

