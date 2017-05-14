# -*- coding: utf-8 -*-
"""
Este módulo contém funções e classes que permitem obter e manipular
estimativas de horários de chegadas de ônibus nos pontos da cidade de Vítória.

As informações são obtidas diretamente do serviço Ponto Vitória e do site da PMV.
"""

import urllib2
import json
from unicodedata import normalize

from services import ItinerariosPMV
from main import main


class cLinhaDeOnibus:
    """Armazena informações sobre linhas de ônibus"""
    def __init__(self, id, Bandeira, Numero):
        self.id = id
        self.Bandeira = Bandeira
        self.Numero = Numero


class cPontoDeOnibus:
    """Armazena informações sobre pontos de ônibus"""
    def __init__(self, id, NumeroIdentificacao, Logradouro, PontoDeReferencia):
        self.id = id
        self.Numero = NumeroIdentificacao
        self.Logradouro = Logradouro
        self.PontoDeReferencia = PontoDeReferencia


class cEstimativa:
    """Armazena estimativas de horários de chegada de uma determinada linha"""
    def __init__(self):
        self.acessibilidade = False;
        self.Linha = None
        self.HorarioDePartida = 0
        self.HorarioDaTransmissao = 0
        self.HorarioDeChegada = 0
        self.Itinerarioid = 0


def obter_estimativas_de_ponto(pontoIdentificador):
    """Retorna estimativas de horário de chegada de todos os ônibus em um ponto 
    
    :param pontoIdentificador: Numero de identificação do ponto do qual se deseja obter as estimativas
    
    :returns: Retorna um dicionário de estimativas cujo a chave é uma tupple no formato (NumeroDaLinha, Bandeira)
    e os itens são listas de objetos do tipo cEstimativa pertencentes a cada linha de ônibus 
    """
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)
    
    pontoId = -1

    for pnt in pontosJSON['pontosDeParada']:
        if pnt['identificador'] == pontoIdentificador:
            pontoId = pnt['id']
            break
    
    data = json.dumps({"pontoDeOrigemId":pontoId})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/estimativas/obterEstimativasPorOrigem'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    listaEstimativas = []
    listaItinerarioIds = []
    
    for est in responseJSON['estimativas']:
        Estimativa = cEstimativa()
        Estimativa.acessibilidade = est[u'acessibilidade']
        Estimativa.HorarioDePartida = est[u'horarioDePartida']
        Estimativa.HorarioDaTransmissao = est[u'horarioDaTransmissao']
        Estimativa.HorarioDeChegada = est[u'horarioNaOrigem']
        Estimativa.ItinerarioId = est[u'itinerarioId']
        
        listaEstimativas.append(Estimativa)
        
        listaItinerarioIds.append(Estimativa.ItinerarioId)

    data = json.dumps({"listaIds":listaItinerarioIds})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarItinerarios'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    itinsDict = {}
    dictEstimativas = {}
    
    for itin in responseJSON[u'itinerarios']:
        linha = cLinhaDeOnibus(itin[u'id'], itin[u'bandeira'], itin[u'identificadorLinha'])
        itinsDict[linha.id] = linha
        
    for est in listaEstimativas:
        est.Linha = itinsDict[est.ItinerarioId]
        
        if dictEstimativas.has_key((est.Linha.Numero, est.Linha.Bandeira)):
            dictEstimativas[(est.Linha.Numero, est.Linha.Bandeira)].append(est)
        else:
            dictEstimativas[(est.Linha.Numero, est.Linha.Bandeira)] = []
            dictEstimativas[(est.Linha.Numero, est.Linha.Bandeira)].append(est)
    
    return dictEstimativas
    
def obter_pontos(listaIdentificadores):
    """Retorna informações sobre pontos de ônibus(Logradouro, referência, etc)
    
    :param listaIdentificadores: Lista com os numeros de identificação dos pontos
    dos quais se deseja obter as informações
    
    :returns: lista de objetos do tipo cPontoDeOnibus com as informações sobre cada ponto
    """
    listaDePontosIds = []
            
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)

    for pnt in pontosJSON['pontosDeParada']:
        if pnt['identificador'] in listaIdentificadores:
            listaDePontosIds.append(pnt['id'])
    
    
    data = json.dumps({"listaIds":listaDePontosIds})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarPontosDeParada'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    listaPontosDeParada = []
    
    for ponto in responseJSON['pontosDeParada']:
        listaPontosDeParada.append(cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao']))
        
    return listaPontosDeParada

def pesquisar_ponto(stringDeBusca):
    """Pesquisa por pontos de ônibus utilizando uma string de busca
    
    :param stringDeBusca: string que será utilizada para efetuar a busca no Ponto Vitória
    
    :returns: lista de objetos do tipo cPontoDeOnibus contendo informações sobre os pontos encontrados
    
    """
    data = json.dumps({"texto":stringDeBusca.decode('iso-8859-15')})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/texto/pesquisarPontosDeParada'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    data = json.dumps({"listaIds":responseJSON['pontosDeParada']})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarPontosDeParada'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    listaPontos = []
        
    for ponto in responseJSON[u'pontosDeParada']:
        pnt = cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao'])
        listaPontos.append(pnt)

    return listaPontos

def obter_pontos_de_parada(PontoIdentificador):
    """Busca no Ponto Vitória por pontos que possuem linhas em comum com o ponto cujo identificador
    é passado na função
    
    :param PontoIdentificador: Numero identificador do ponto do qual se deseja obter os pontos em comum
    
    :returns: lista de objetos do tipo cPontoDeOnibus com informações dos pontos que possuem linhas em comum
    """
    listaDePontosIds = []
            
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)

    for pnt in pontosJSON['pontosDeParada']:
        if pnt['identificador'] == PontoIdentificador:
            PontoId = pnt['id']
            break

    data = json.dumps({"pontoDeOrigemId":PontoId})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/pesquisarPontosDeParada'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    data = json.dumps({"listaIds":responseJSON['pontosDeParada']})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarPontosDeParada'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    listaPontos = []
        
    for ponto in responseJSON[u'pontosDeParada']:
        pnt = cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao'])
        listaPontos.append(pnt)

    return listaPontos
    
def obter_itinerario_de_linha(cdLinha):
    """Retorna os pontos de ônibus que fazem parte do itinerário de determinada linha
    
    :param cdLinha: Numero da linha da qual se deseja obter o itinerario
    
    :returns: Lista com objetos do tipo cPontoDeOnibus representando todos os pontos 
    que fazem parte do itinerario da linha
    
    """
    Itin = ItinerariosPMV.Itinerario(str(cdLinha).zfill(4))
    pontosDoItinerario = []
    TodosOsPontos = ObterTodosOsPontos()
    pntosRuaDoItinerario = []
    
    ItinCopy = []
    
    print 'Pesquisando Itinerario da linha... Aguarde'
    
    #removendo acentos
    for it in set(Itin):
        ItinCopy.append(normalize('NFKD', it.decode('utf-8')).encode('ASCII','ignore').lower())
    
    #buscando pontos que estao presentes nas ruas em que o onibus passa
    for ponto in TodosOsPontos:
        pontoLogradouro = normalize('NFKD', ponto.Logradouro).encode('ASCII','ignore').lower()
        
        if pontoLogradouro in ItinCopy:
            pntosRuaDoItinerario.append(ponto)
    
    
    #Analisando onibus que passam nesses pontos e verificando se a linha informada passa por eles
    for ponto in pntosRuaDoItinerario:
        if len(ExtraiEstimativasDeLinha(str(cdLinha).zfill(3), ObterEstimativasDePonto(ponto.id))) != 0:
            pontosDoItinerario.append(ponto)
    
    return pontosDoItinerario
    
def obter_todos_os_pontos():
    """Retorna uma lista de objetos do tipo cPontoDeOnibus representando todos os pontos da cidade.
    
    As informações são extraídas do arquivo JSON presente na pasta JSON/PontosDeOnibusVitoria.json
    
    """
    pontos = []
    
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)
    
    for pnt in pontosJSON['pontosDeParada']:
        p = cPontoDeOnibus(pnt['id'], pnt['identificador'], pnt['logradouro'], pnt['descricao'])        
        pontos.append(p)
    
    return pontos
    
