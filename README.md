# Itinerário Vitória

Um módulo python que contém funções e classes que permitem a manipulação e obtenção de informações sobre as linhas de ônibus e pontos da cidade de Vitória, bem como previsões de horários de chegada dos ônibus nesses pontos. As informações são obtidas do serviço **Ponto Vitória** e do site da PMV.

## Utilização

O módulo contém um script(main.py) para permitir o uso de algumas funções básicas pelo terminal. O comando abaixo, por exemplo, permite visualizar as previsões de chegada da linha 074 - Tabuazeiro/Circular no ponto 4046.
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

## Autores

Desenvolvido por **Gean Paulo** - Email: gean.2007.8.9.0@gmail.com

## Licença

Esse projeto está licenciado sob a licença MIT - leia o arquivo LICENSE.TXT

