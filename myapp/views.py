from django.shortcuts import render
from pathlib import Path
import json
import os

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def mysite(request):
    if request.method == 'POST' and request.FILES.get('diretorio'):
        
        diretorio = request.FILES['diretorio']
        # Aqui você pode processar o diretório selecionado
        response_content = "Arquivos no diretório selecionado:\n"
        for arquivo in diretorio:
            response_content += f"- {arquivo}\n"
        print(request.FILES['diretorio']['TemporaryUploadedFile'])
        
        return HttpResponse(request.FILES['diretorio'])
    
    return render(request, 'index.html')