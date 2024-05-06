from django import forms
from django.forms import ClearableFileInput
from .models import UploadArquivos

class MeuFormulario(forms.ModelForm):
    class Meta:
        model = UploadArquivos
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
        }