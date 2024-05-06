from django.db import models
from django import forms

class UploadArquivos(models.Model):
    arquivo = models.FileField(upload_to='arquivos/', blank=True, null=True)
    # arquivo = forms.FileField(upload_to='arquivos', widget = forms.TextInput(attrs={
    #         "name": "images",
    #         "type": "File",
    #         "class": "form-control",
    #         "multiple": "True",
    #     }), label = "")
