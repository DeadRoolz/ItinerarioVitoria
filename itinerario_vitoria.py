# -*- coding: utf-8 -*-
"""
Este módulo contém funções e classes que permitem obter e manipular
estimativas de horários de chegadas de ônibus nos pontos da cidade de Vítória.

As informações são obtidas diretamente do serviço Ponto Vitória e do site da PMV.
"""

import urllib2
import json
from unicodedata import normalize
import datetime

from cli import *


class cLinhaDeOnibus:
    """Armazena informações sobre linhas de ônibus"""
    
    def __init__(self, Id, Bandeira, Numero):
        self.Id = Id
        self.Bandeira = Bandeira
        self.Numero = Numero
        
    def bandeira(self):
        return self.Bandeira
        
    def numero(self):
        return self.Numero
    def id(self):
        return self.Id


class cPontoDeOnibus:
    """Armazena informações sobre pontos de ônibus"""
    
    def __init__(self, _Id, _NumeroIdentificacao, _Logradouro, _PontoDeReferencia, _linhas):
        self.Id = _Id
        self.Numero = _NumeroIdentificacao
        self.Logradouro = _Logradouro
        self.PontoDeReferencia = _PontoDeReferencia
        self.Linhas = _linhas
        
    def linhas(self):
        return self.Linhas
        
    def numero(self):
        return self.Numero
    
    def logradouro(self):
        return self.Logradouro
    
    def referencia(self):
        return self.PontoDeReferencia


class cEstimativa:
    """Armazena estimativas de horários de chegada de uma determinada linha"""
    
    def __init__(self, _acess, _linha, _horaPartida, _horaTransmissao, _horaChegada, _itinId):
        self.Acessibilidade = _acess;
        self.Linha = _linha
        self.HorarioDePartida = datetime.datetime.fromtimestamp(_horaPartida/1000)
        self.HorarioDaTransmissao = datetime.datetime.fromtimestamp(_horaTransmissao/1000)
        self.HorarioDeChegada = datetime.datetime.fromtimestamp(_horaChegada/1000)
        self.ItinerarioId = _itinId
        
    def acessibilidade(self):
        return self.Acessibilidade
    
    def linha(self):
        return self.Linha
    
    def linha_bandeira(self):
        return self.linha().bandeira()
        
    def linha_numero(self):
        return self.linha().numero()
        
    def horario_partida(self):
        return self.HorarioDePartida
        
    def horario_transmissao(self):
        return self.HorarioDaTransmissao
        
    def horario_chegada(self):
        return self.HorarioDeChegada
    
    def set_linha(self, _linha):
        self.Linha = _linha
        
    def itinerario_id(self):
        return self.ItinerarioId
        


def obter_estimativas_de_ponto(pontoIdentificador):
    """Retorna estimativas de horário de chegada de todos os ônibus em um ponto 
    
    :param pontoIdentificador: Numero de identificação do ponto do qual se deseja obter as estimativas
    
    :returns: Retorna uma lista de objetos do tipo cEstimativa 
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
        Estimativa = cEstimativa(est[u'acessibilidade'], None, est[u'horarioDePartida'], est[u'horarioDaTransmissao'], est[u'horarioNaOrigem'], est[u'itinerarioId'])
        
        listaEstimativas.append(Estimativa)
        
        listaItinerarioIds.append(Estimativa.itinerario_id())

    data = json.dumps({"listaIds":listaItinerarioIds})
    url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarItinerarios'
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    responseJSON = json.load(f)
    f.close()
    
    itinsDict = {}
    
    for itin in responseJSON[u'itinerarios']:
        linha = cLinhaDeOnibus(itin[u'id'], itin[u'bandeira'], itin[u'identificadorLinha'])
        itinsDict[linha.id()] = linha
        
    for est in listaEstimativas:
        est.set_linha(itinsDict[est.itinerario_id()])
    
    return listaEstimativas
    
def obter_pontos(listaIdentificadores):
    """Retorna informações sobre pontos de ônibus(Logradouro, referência, etc)
    
    :param listaIdentificadores: Lista com os numeros de identificação dos pontos
    dos quais se deseja obter as informações
    
    :returns: lista de objetos do tipo cPontoDeOnibus com as informações sobre cada ponto
    """
            
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)
    
    listaPontosDeParada = []

    for ponto in pontosJSON['pontosDeParada']:
        if ponto['identificador'] in listaIdentificadores:
            listaPontosDeParada.append(cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao'], ponto['linhas']))
        
        
    return listaPontosDeParada

def pesquisar_pontos(stringDeBusca):
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
    
    listaIds = responseJSON['pontosDeParada']
    
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)
    
    listaPontos = []
        
    for ponto in pontosJSON['pontosDeParada']:
        if ponto['id'] in listaIds:
            pnt = cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao'], ponto['linhas'])
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
        pnt = cPontoDeOnibus(ponto['id'], ponto['identificador'], ponto['logradouro'], ponto['descricao'], ponto['linhas'])
        listaPontos.append(pnt)

    return listaPontos
    
def obter_itinerario_de_linha(cdLinha):
    """Retorna os pontos de ônibus que fazem parte do itinerário de determinada linha
    
    :param cdLinha: Numero da linha da qual se deseja obter o itinerario
    
    :returns: Lista com objetos do tipo cPontoDeOnibus representando todos os pontos 
    que fazem parte do itinerario da linha
    
    """
    
    pontosDoItinerario = []
    
    for ponto in obter_todos_os_pontos():
        if cdLinha in ponto.linhas():
            pontosDoItinerario.append(ponto)
    
    return pontosDoItinerario
    
def obter_todos_os_pontos():
    """Retorna uma lista de objetos do tipo cPontoDeOnibus representando todos os pontos da cidade.
    
    As informações são extraídas do arquivo JSON presente na pasta JSON/PontosDeOnibusVitoria.json
    
    :returns: Lista com objetos do tipo cPontoDeOnibus representando todos os pontos da cidade.
    
    """
    pontos = []
    
    pontosFile = open('JSON/PontosDeOnibusVitoria.json')
    pontosJSON = json.load(pontosFile)
    
    for pnt in pontosJSON['pontosDeParada']:
        p = cPontoDeOnibus(pnt['id'], pnt['identificador'], pnt['logradouro'], pnt['descricao'], pnt['linhas'])        
        pontos.append(p)
    
    return pontos
    
if __name__ == "__main__":
    cli(sys.argv[1:])