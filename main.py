# -*- coding: utf-8 -*-
"""
usage: main.py [-h] [-p NUMEROIDENTIFICADOR [NUMEROIDENTIFICADOR ...]]
               [-l NUMERO [NUMERO ...]] [-e] [-i] [-s KEYWORD]

Exibe estimativas de horarios de chegada dos onibus municipais nos pontos da
cidade de Vitoria. As informacoes sao extraidas do Ponto Vitoria e do site da
PMV.

optional arguments:
  -h, --help            show this help message and exit
  -p NUMEROIDENTIFICADOR [NUMEROIDENTIFICADOR ...], --ponto NUMEROIDENTIFICADOR [NUMEROIDENTIFICADOR ...]
                        O numero identificador do ponto em que se deseja
                        buscar informacoes ou obter estimativas.
  -l NUMERO [NUMERO ...], --linha NUMERO [NUMERO ...]
                        O numero da linha em que se deseja buscar informacoes
                        ou obter estimativas.
  -e, --estimativas     Mostra previsoes de chegadas de onibus em pontos. Os
                        pontos e as linhas de onibus devem ser informados
                        utilizando as opcoes: -l ou --linha e -p ou --ponto.
  -i, --itinerario      Procura e exibe os pontos que fazem parte do
                        itinerario da(s) linha(s) informadas pelas opcoes: -l
                        ou --linha.
  -s KEYWORD, --pesquisar KEYWORD
                        Pesquisa por pontos de onibus utilizando "KEYWORD"
                        como palavra-chave

"""

import datetime
import sys
import argparse

from itinerario_vitoria import *

def main(argv):
    
        
    parser = argparse.ArgumentParser(description = u'Exibe estimativas \
                                                    de horarios de chegada dos onibus municipais nos \
                                                    pontos da cidade de Vitoria. \
                                                    As informacoes sao extraidas do Ponto Vitoria e do site da PMV.')
    
    parser.add_argument('-p', '--ponto', action = 'store', dest = 'NumeroIdentificador', 
                        type=str, nargs='+', default = [], required = False,
                           help = 'O numero identificador do ponto em que se deseja buscar informacoes ou obter estimativas.')
    
    parser.add_argument('-l', '--linha', action = 'store', dest = 'Numero', type=str, nargs='+',
                           default = [], required = False,
                           help = 'O numero da linha em que se deseja buscar \
                                    informacoes ou obter estimativas.')
    
    parser.add_argument('-e', '--estimativas', action = 'store_true', required = False, dest='ObterEstimativas',
                           help = 'Mostra previsoes de chegadas de onibus em pontos. \
                                    Os pontos e as linhas de onibus devem ser informados utilizando as opcoes: -l ou --linha e -p ou --ponto.')

    parser.add_argument('-i', '--itinerario', action = 'store_true', required = False, dest='ObterItinerario',
                           help = 'Procura e exibe os pontos que fazem parte do itinerario da(s) linha(s) \
                                    informadas pelas opcoes: -l ou --linha.')
    
    parser.add_argument('-s', '--pesquisar', action = 'store', required = False, dest='keyword', type=str,
                            default = '', help = 'Pesquisa por pontos de onibus \
                                                    utilizando "KEYWORD" como palavra-chave')
    
    args = vars(parser.parse_args(argv))
    
    listaDePontos = args['NumeroIdentificador']
    listaDeLinhas = args['Numero']
    stringDeBusca = args['keyword']
    
    #print args
    
    if (len(listaDePontos) > 0) and (len(listaDeLinhas) <= 0):
        
        pontos = obter_pontos(listaDePontos)
        
        
        if (args['ObterEstimativas'] == False):
            
            for ponto in pontos:
                print 'Numero: ' + str(ponto.Numero)
                print 'Logradouro: ' + ponto.Logradouro
                print 'Ponto de Referencia: ' + ponto.PontoDeReferencia
                print '----------------------------------------------------------'
        
        else:
            
            ListaDeEstimativas = []
            
            for ponto in pontos:
                print 'Numero: ' + str(ponto.Numero)
                print 'Logradouro: ' + ponto.Logradouro
                print 'Ponto de Referencia: ' + ponto.PontoDeReferencia
                print ''
                
                dictEstimativas = obter_estimativas_de_ponto(ponto.Numero)
                
                for key in dictEstimativas.keys():
                    
                    print '---------------------------------------------------------------------'
                    print '> Linha: ' + key[0] + ' - ' + key[1]
                    print '---------------------------------------------------------------------'
                    
                    for estimativa in sorted(dictEstimativas[key], key=lambda est: est.HorarioDeChegada):                        
                        print '>> ' + 'acessibilidade: ' + str(estimativa.acessibilidade)
                        print '>> ' + 'Horario de Chegada: ' + datetime.datetime.fromtimestamp(estimativa.HorarioDeChegada/1000).ctime()
                        print ''
                
        
        print '-FIM-'
        
    elif (len(stringDeBusca) >= 4) and (len(listaDePontos) <= 0) and (len(listaDeLinhas) <= 0):
        pontos = pesquisar_ponto(stringDeBusca)
            
        for ponto in pontos:
            print 'Numero: ' + str(ponto.Numero)
            print 'Logradouro: ' + ponto.Logradouro
            print 'Ponto de Referencia: ' + ponto.PontoDeReferencia
            print '----------------------------------------------------------'
        
        print '-FIM-'
        
    elif (len(listaDeLinhas) > 0):
        
        if (len(listaDePontos) > 0) and ((args['ObterEstimativas'] == True)):
            
            pontos = obter_pontos(listaDePontos)
            
            for NumeroLinha in listaDeLinhas:
                for ponto in pontos:
                    
                    print 'Numero: ' + str(ponto.Numero)
                    print 'Logradouro: ' + ponto.Logradouro
                    print 'Ponto de Referencia: ' + ponto.PontoDeReferencia
                    
                    dictEstimativas = obter_estimativas_de_ponto(ponto.Numero)
                    
                    for key in dictEstimativas.keys():
                        if key[0] == NumeroLinha:
                            print '---------------------------------------------------------------------'
                            print '> Linha: ' + key[0] + ' - ' + key[1]
                            print '---------------------------------------------------------------------'
                    
                            for estimativa in sorted(dictEstimativas[key], key=lambda est: est.HorarioDeChegada):                        
                                print '>> ' + 'acessibilidade: ' + str(estimativa.acessibilidade)
                                print '>> ' + 'Horario de Chegada: ' + datetime.datetime.fromtimestamp(estimativa.HorarioDeChegada/1000).ctime()
                                print ''
    
        print '-FIM-'
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])
