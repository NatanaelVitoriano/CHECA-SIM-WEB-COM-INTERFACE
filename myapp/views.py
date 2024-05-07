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
    dataNE = []
    dataLI = []
    dataCO = []
    
    if request.method == 'POST' and request.FILES.get('diretorio'):
        arquivos = request.FILES.getlist('diretorio')
        # Aqui você pode processar o diretório selecionado
        
        response_content = "Arquivos no diretório selecionado:\n"
        for arquivo in arquivos:
            # print(arquivo)
            if 'NE2' in str(arquivo):
                for linhaDoNE in arquivo:
                    print(arquivo.readline())
                    dataNE.append(linhaDoNE)
            if 'LI2' in str(arquivo):
                for linhaDoLI in arquivo:
                    dataLI.append(linhaDoLI)
            if 'CO2' in str(arquivo):
                for linhaDoCO in arquivo:
                    dataCO.append(linhaDoCO)
                    
        # Retornar a resposta HTTP com a lista de arquivos
        return HttpResponse(response_content)
    
    return render(request, 'index.html')
