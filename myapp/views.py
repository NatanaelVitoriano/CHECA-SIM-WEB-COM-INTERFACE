from django.shortcuts import render
from django.http import HttpResponseRedirect
from pathlib import Path
import os
from .forms import MeuFormulario
from .models import UploadArquivos

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def mysite(request):
    
    if request.method == 'POST' and request.FILES.get('diretorio'):
        arquivos = request.FILES.getlist('diretorio')
        # Aqui você pode processar o diretório selecionado

        # Exemplo de processamento do diretório (simulado)
        arquivos_no_diretorio = ['arquivo1.txt', 'arquivo2.txt', 'arquivo3.txt']

        # Construir uma string com os nomes dos arquivos
        response_content = "Arquivos no diretório selecionado:\n"
        for arquivo in arquivos:
            print(arquivo.readline())
            response_content += f"- {arquivo.readline()}\n"

        # Retornar a resposta HTTP com a lista de arquivos
        return HttpResponse(response_content)
    
    return render(request, 'index.html')
