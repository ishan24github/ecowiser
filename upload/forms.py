from django import forms
from .models import UploadedVideo


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo
        fields = ['video']


class WordForm(forms.Form):
    search_keyword = forms.CharField(max_length=50)

   