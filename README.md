# Itinerário Vitória

Um módulo python que contém funções e classes que permitem a manipulação e obtenção de informações sobre as linhas de ônibus e pontos da cidade de Vitória, bem como previsões de horários de chegada dos ônibus nesses pontos. As informações são obtidas do serviço [Ponto Vitória](http://sistemas.vitoria.es.gov.br/pontovitoria/) e do [site de consultas de itinerários de ônibus municipais da PMV](http://sistemas.vitoria.es.gov.br/redeiti).

## Utilização

O módulo contém um script(main.py) que permite fazer o uso de algumas funções básicas pelo terminal. O comando abaixo, por exemplo, permite visualizar os horários previstos de chegada da linha 074 - Tabuazeiro/Circular no ponto 4046.
```
python main.py -e -p 4046 -l 074
```
O trecho de código abaixo mostra um exemplo de uso da função obter\_estimativas\_de\_ponto que retorna um dicionário contendo estimativas de horários de chegada das linhas que passam naquele ponto:

```python
from itinerario_vitoria import *
import datetime

dictEstimativas = obter_estimativas_de_ponto('4046')
for key in dictEstimativas.keys():
    print '---------------'
    print 'Linha: ' + key[0] + ' - ' + key[1]
    print '---------------'
    
    for estimativa in dictEstimativas[key]:
        print 'Horario de Chegada: ' + datetime.datetime.fromtimestamp(estimativa.HorarioDeChegada/1000).ctime()
	print ''
```

## Contribuindo

Qualquer pessoa pode contribuir com o projeto, adicionando novas funcionalidades, corrigindo bugs, sugerindo algoritmos para melhorar o desempenho e etc.

Caso queira contribuir crie uma [Issue](https://github.com/DeadRoolz/ItinerarioVitoria/issues) ou faça um [Pull Request](https://github.com/DeadRoolz/ItinerarioVitoria/pulls)


## Referência da API

* [Classes](#Classes)
* [Métodos](#Métodos)

### Classes

\# _cLinhaDeOnibus_
Classe que representa as linhas de ônibus.

Atributos: 
* `id` - id da linha - Tipo: _int_
* `Bandeira` - bandeira do ônibus(nome da linha) - Tipo: _str_
* `Numero` - numero da linha - Tipo: _str_

\# _cPontoDeOnibus_
Classe que representa os pontos de ônibus.

Atributos: 
* `id` - id do ponto - Tipo: _int_
* `Numero` - Número de identificação do ponto - Tipo: _str_
* `Logradouro` - logradouro em que o ponto está situado - Tipo: _str_
* `PontoDeReferencia` - Ponto de referência próximo - Tipo: _str_

\# _cEstimativa_
Classe que representa estimativas de horários de chegada dos ônibus.

Atributos: 
* `acessibilidade` - indica se o ponto possui acessibilidade para deficientes - Tipo: _Boolean_
* `Linha` - Objeto que representa a linha de ônibus pertencente à estimativa - Tipo: _cLinhaDeOnibus_
* `HorarioDePartida` - horário de partida do ônibus no ponto final (formato unix timestamp em milisegundos)  - Tipo: _int_
* `HorarioDeTransmissao` - último horário em que o ônibus transmitiu sua localização (formato unix timestamp em milisegundos)  - Tipo: _int_
* `HorarioDeChegada` - horário previsto de chegada no ponto (formato unix timestamp em milisegundos)  - Tipo: _int_
* `Itinerarioid` - id da linha de ônibus ligada à estimativa  - Tipo: _int_


## Autores

Desenvolvido por **Gean Paulo** - Email: gean.2007.8.9.0@gmail.com

## Licença

Esse projeto está licenciado sob a licença MIT - leia o arquivo LICENSE.TXT