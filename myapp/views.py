from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from pathlib import Path
import requests
import json
import os
from .forms import MeuFormulario
from .models import UploadArquivos
from django.http import HttpResponse

dataNE = []
dataLI = []
dataCO = []
listaDeContratosNaAPI = []
listaDeLicitacoesNaAPI = []
licitacoesEmpenhadas = []
listaDeLicitacoesNoLI = []
listaDeLicitacoesNoSIMWEB = []
logContent = []

def mysite(request):
    return render(request, 'index.html')

def exibir_resultado(request):
    if request.method == 'POST' and request.FILES.get('diretorio'):
        arquivos = request.FILES.getlist('diretorio')
        validarArquivosSIM(arquivos)
        # logFormatado = "\n".join(logContent)
        return render(request, 'resultado.html', {'lista': logContent})
    
    else:
        return redirect('mysite')
    
def validarArquivosSIM(arquivos):
    varClear()
    lerArquivosDoSIM(arquivos)
    apiJson = buscarDadosNaAPI(municipio)
    listaDeContratosNaAPI = apiJson[0]
    listaDeLicitacoesNaAPI = apiJson[1]
    
    for licitacaoLI in dataLI:
        listaDeLicitacoesNoSIMWEB.append([licitacaoLI[3].replace('"',""),licitacaoLI[2]])

    for licitacao in listaDeLicitacoesNaAPI:
        listaDeLicitacoesNoSIMWEB.append([licitacao['numero_licitacao'].replace('"',""), licitacao["data_realizacao_autuacao_licitacao"].replace('"',"").replace("-","")])
    
    licitacaoFaltando = True
    numLicitacaoFaltando = ''
    for x, data in enumerate(dataNE, start=1):
        if data[24].replace('"', '') == "":
            continue
                
        licitacaoFaltando = True 
        for i in listaDeLicitacoesNoSIMWEB:
            if data[26].replace('"',"") == i[0] and data[27].replace('"',"") == i[1]:
                licitacaoFaltando = False 
                break
        
        if licitacaoFaltando:
            logContent.append(f"Licitação faltando no arquivo LI, na linha {x} do arquivo NE: {data[26]}")
        
    for licitacaoLI in dataLI:
        for licitacao in listaDeLicitacoesNaAPI:
            if licitacaoLI[3].replace('"',"") == licitacao['numero_licitacao']:
                logContent.append("Licitacao " + licitacaoLI[3] + " duplicada")
                
    for x, ctCO in enumerate(dataCO, start= 1):
        if ctCO[20].replace('"',"") == "":
            continue
        
        licitacaoNoSIM = False
        licitacaoNoArquivoLI = False
        while True:
            for licitacaoApi in listaDeLicitacoesNaAPI:
                if ctCO[20].replace('"',"") == licitacaoApi['numero_licitacao'].replace('"',"") and ctCO[19] == licitacaoApi["data_realizacao_autuacao_licitacao"].replace('"',"").replace("-",""):
                    licitacaoNoSIM = True
                    break
                
            for licitacaoLI in dataLI:
                if ctCO[20].replace('"',"") == licitacaoLI[3].replace('"',"") and ctCO[19] == licitacaoLI[2]:
                    
                    licitacaoNoArquivoLI = True
                    break
                
            if licitacaoNoSIM == False and licitacaoNoArquivoLI == False:
                logContent.append("Licitacao no arquivo CO na linha " + str(x) +  " não existe no arquivo LI, NE e APITCE: " + ctCO[20])
            
            else:
                break
            
            break
        
    #Checando contratos
    for x, dadosCO in enumerate(dataNE, start=1):
        if dadosCO[24].replace('"', '') == "":
            continue
        
        while True:
            contratoNoSIM = False
            contratoNoArquivoCO = False
            temEmpenho = True
            for i, contrato in enumerate(listaDeContratosNaAPI, start=0):
                if dadosCO[24].replace('"',"") == contrato['numero_contrato'].replace('"',"") and dadosCO[25].replace('"',"") == contrato['data_contrato'].replace("-","")[0:8]:
                    contratoNoSIM = True
                    
                    # print(contrato['numero_contrato'])
                elif dadosCO[24].replace('"',"") == contrato['numero_contrato'].replace('"',"") and dadosCO[25].replace('"',"") != contrato['data_contrato'].replace("-","")[0:8]:
                    logContent.append("Contrato " + dadosCO[24] + " com data diferente")
                    
                    
            for i, contratoCO in enumerate(dataCO, start=0):
                    
                    if dadosCO[24].replace('"',"") == contratoCO[3].replace('"',"") and dadosCO[25].replace('"',"") == contratoCO[4].replace('"',""):
                        contratoNoArquivoCO = True
                        temEmpenho = True
                        break
                        
                    
                    elif dadosCO[24].replace('"',"") == contratoCO[3].replace('"',"") and dadosCO[25].replace('"',"") != contratoCO[4].replace('"',""):
                        logContent.append("Contrato " + dadosCO[24] + " com data diferente")
                        temEmpenho = True
                        break
                        
                        
                    elif dadosCO[24].replace('"',"") != contratoCO[3].replace('"',"") and dadosCO[25].replace('"',"") != contratoCO[4].replace('"',""):
                        contratoNoArquivoCO = False
                        
            if contratoNoSIM and contratoNoArquivoCO:
                logContent.append("Contrato " + dadosCO[24].replace('"',"") + " na linha " + str(x) + " do arquivo NE está duplicado.")
                
            elif contratoNoSIM and contratoNoArquivoCO == False:
                pass
                    
            elif contratoNoSIM == False and contratoNoArquivoCO == False:
                logContent.append("Contrato faltando no arquivo CO, na linha " + str(x) + " do arquivo NE: " + dadosCO[24])
            
            elif contratoNoSIM == False and contratoNoArquivoCO and temEmpenho == False:
                logContent.append("sem empenho")
            
            elif contratoNoSIM == False and contratoNoArquivoCO == True:
                pass
            
            else:
                logContent.append("Contrato " + dadosCO[24].replace('"',"") + " invalido")
            break
    checarSeTemEmpenho()
    
def varClear():
    global dataNE
    global dataLI
    global dataCO
    global listaDeContratosNaAPI
    global listaDeLicitacoesNaAPI
    global licitacoesEmpenhadas
    global listaDeLicitacoesNoLI
    global listaDeLicitacoesNoSIMWEB
    global logContent
    
    dataNE.clear()
    dataLI.clear()
    dataCO.clear()
    listaDeContratosNaAPI.clear()
    listaDeLicitacoesNaAPI.clear()
    licitacoesEmpenhadas.clear()
    listaDeLicitacoesNoLI.clear()
    listaDeLicitacoesNoSIMWEB.clear()
    logContent.clear()
    
def checarSeTemEmpenho():
    for contratoCO in dataCO:
        if not(str(contratoCO[3]) in str(dataNE)):
            logContent.append("Contrato " + contratoCO[3] + " sem empenho no arquivo NE.")
        
    for dadosLI in dataLI:
        if not(str(dadosLI[3]) in str(dataNE)):
            logContent.append("Licitacao " + dadosLI[3] + " sem empenho no arquivo NE.")
            
def lerArquivosDoSIM(arquivos):
    global municipio
    for arquivo in arquivos:
            if 'NE2' in str(arquivo):
                for linhaDoNE in arquivo:
                    dataNE.append(linhaDoNE.decode("utf-8").replace("\r\n", "").split(","))
                
            if 'LI2' in str(arquivo):
                for linhaDoLI in arquivo:
                    dataLI.append(linhaDoLI.decode("utf-8").replace("\r\n", "").split(","))
                    
            if 'CO2' in str(arquivo):
                for linhaDoCO in arquivo:
                    dataCO.append(linhaDoCO.decode("utf-8").replace("\r\n", "").split(","))
    municipio = dataNE[0][1].replace('"',"")

def buscarDadosNaAPI(municipio):
    try:
        rLicitacao = requests.get('https://api-dados-abertos.tce.ce.gov.br/licitacoes?codigo_municipio=' + municipio + '&data_realizacao_autuacao_licitacao=2010-01-01_2030-12-31')
        rContratos = requests.get('https://api-dados-abertos.tce.ce.gov.br/contrato?codigo_municipio=' + municipio + '&data_contrato=2010-01-01_2030-12-31&quantidade=0&deslocamento=0')
    except:
        print("Tentando conexao com API TCE...")
        try:
            rLicitacao = requests.get('https://api-dados-abertos.tce.ce.gov.br/licitacoes?codigo_municipio=' + municipio + '&data_realizacao_autuacao_licitacao=2010-01-01_2030-12-31')
            rContratos = requests.get('https://api-dados-abertos.tce.ce.gov.br/contrato?codigo_municipio=' + municipio + '&data_contrato=2010-01-01_2030-12-31&quantidade=0&deslocamento=0')
        except:
            print("Não foi possivel conectar-se a API.")
            os.system("PAUSE")
            quit()
            
    json = rLicitacao.json()
    listaDeLicitacoes = json['data']

    json = rContratos.json()
    listaDeContratos = json['data']
    
    return listaDeContratos, listaDeLicitacoes
