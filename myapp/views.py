from django.shortcuts import render
from django.http import HttpResponseRedirect
from pathlib import Path
import os
from .forms import MeuFormulario
from .models import UploadArquivos

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def upload_arquivo(request):
    if request.method == 'POST':
        formulario = MeuFormulario(request.POST, request.FILES)
        files = request.FILES.getlist('arquivo')
        if formulario.is_valid():
            for f in files:
                file_instance = UploadArquivos(arquivo=f)
                file_instance.save()
            # return render(request, 'index.html')
    else:
        
        formulario = MeuFormulario()
    
    return render(request, 'upload_form.html', {'formulario': formulario})

def mysite(request):
    
    if request.method == 'POST' and request.FILES.get('diretorio'):
        diretorio = request.FILES.getlist('diretorio')
        # Aqui você pode processar o diretório selecionado

        # Exemplo de processamento do diretório (simulado)
        arquivos_no_diretorio = ['arquivo1.txt', 'arquivo2.txt', 'arquivo3.txt']

        # Construir uma string com os nomes dos arquivos
        response_content = "Arquivos no diretório selecionado:\n"
        for arquivo in diretorio:
            response_content += f"- {arquivo}\n"

        # Retornar a resposta HTTP com a lista de arquivos
        return HttpResponse(response_content)
    
    return render(request, 'index.html')
