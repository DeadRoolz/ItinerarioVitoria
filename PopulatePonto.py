# -*- coding: utf-8 -*-

'''
Identifica quais linhas de onibus passam nos pontos e grava
nos pontos do arquivo PontosDeOnibusVitoria.json numa array chamada 'linhas'
'''

from __future__ import print_function

from itinerario_vitoria import *
import json


envelope = [-40.37534, -20.33324, -40.19137, -20.21865]

print('Numero de pontos armazenados atualmente no arquivo json: ', len(obter_todos_os_pontos()))
print()

print('Baixando todos os pontos de onibus...', end = ' ')

data = json.dumps({"envelope":envelope})
url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/pesquisarPontosDeParada'
req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
f = urllib2.urlopen(req)
responseJSON = json.load(f)
f.close()

data = json.dumps({"listaIds":responseJSON['pontosDeParada']})
url = 'https://pmv.geocontrol.com.br/pontovitoria/svc/json/db/listarPontosDeParada'
req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
f = urllib2.urlopen(req)
pontosJSON = json.load(f)
f.close()

print('[FEITO]')

size = len(pontosJSON['pontosDeParada'])
count = 0

for ponto in pontosJSON['pontosDeParada']:

    count = count+1
    print('\rGravando linhas: ', count, ' de ', size, ' pontos', '| Ponto atual: ', ponto['identificador'] , end='')
    
    estimativas = obter_estimativas_de_ponto(ponto['identificador'])
    
    ponto['linhas'] = []
    
    for est in estimativas:
        if est.linha_numero() not in ponto['linhas']:
            ponto['linhas'].append(est.linha_numero())

print(u'Gravando informações no arquivo...')
f = open('JSON/PontosDeOnibusVitoria.json', 'w')
f.write(json.JSONEncoder().encode(pontosJSON))
print ('\nFeito!')