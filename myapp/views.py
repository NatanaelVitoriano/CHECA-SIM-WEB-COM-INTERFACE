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
            if 'NE2' in str(arquivo):
                dataNEDuplicada = []
                for linhaDoNE in arquivo:
                    # print(linhaDoNE)
                    dataNE.append(linhaDoNE.decode("utf-8").replace("\r\n", "").split(","))
                # dataNE = list(set(dataNEDuplicada))
            if 'LI2' in str(arquivo):
                for linhaDoLI in arquivo:
                    dataLI.append(linhaDoLI.decode("utf-8").replace("\r\n", "").split(","))
                print(len(dataLI))
            if 'CO2' in str(arquivo):
                for linhaDoCO in arquivo:
                    dataCO.append(linhaDoCO.decode("utf-8").replace("\r\n", "").split(","))
            
        # Retornar a resposta HTTP com a lista de arquivos
        return HttpResponse(response_content)
    
    return render(request, 'index.html')
