# -*- coding: utf-8 -*-

"""
Extrai informações sobre os itinerarios dos onibus do 
site da PMV
"""

import urllib2
from HTMLParser import HTMLParser


class SiteItinerarioPMV(HTMLParser):
    
    def __init__(self, srvc):
        HTMLParser.__init__(self)
        self.Found = False
        self.FoundcdLinhaOption = False
        self.ListaDeLinhas = []
        self.Itinerario = []
        self.Finished = False
        self.srvc = srvc
        self.FoundViaLink = False
    
    def handle_starttag(self, tag, attrs):
    
        if self.srvc == 0:
            if self.Found == True:
                if tag == 'option' and attrs[0][1] != '0':
                    self.FoundcdLinhaOption = True
                    if self.Finished != True:
                        self.ListaDeLinhas.append(attrs[0][1])
                else:
                    self.FoundcdLinhaOption = False
            
            if tag == 'select':
                if attrs[0][0] == 'name' and attrs[0][1] == 'cdLinha':
                    self.Found = True
        
        elif self.srvc == 1:
            if tag == 'a' and 'listarLinhas.cfm' in attrs[0][1]:
                self.FoundViaLink = True

    def handle_endtag(self, tag):
        
        if self.srvc == 0:
            if self.Found == True and tag == 'select':
                self.Finished = True

        elif self.srvc == 1:
            pass

    def handle_data(self, data):
        if self.FoundViaLink == True:
            self.Itinerario.append(data)
            self.FoundViaLink = False
        
    def baixar_linhas(self):
        url = 'http://sistemas.vitoria.es.gov.br/redeiti/default.cfm'
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        self.feed(f.read())
        return self.ListaDeLinhas
    
    def baixar_itinerario(self, cdLinha):
        url = 'http://sistemas.vitoria.es.gov.br/redeiti/listarItinerario.cfm?cdLinha=' + cdLinha
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        self.feed(f.read())
        return self.Itinerario

def obter_linhas():
    
    sitePMV = SiteItinerarioPMV(0) # 0 = Baixar Linhas | 1 = Baixar Itinerario de Linha
    return sitePMV.baixar_linhas()

def obter_itinerario(cdLinha):
    sitePMV = SiteItinerarioPMV(1) # 0 = Baixar Linhas | 1 = Baixar Itinerario de Linha
    return sitePMV.baixar_itinerario(str(cdLinha))