# Identificação da Onda Planetária de 2 dias - TCC

## Análise Harmônica

O arquivo `amp.py` realiza a análise harmônica e gera imagens contendo as amplitudes das ondas. No caso específico, ele foi configurado para trabalhar com a onda de 2 dias. A modificação pode ser feita dentro do arquivo control.py, bastando especificar o período a ser trabalhado.

## Espectro de Potência

O espectro de potência foi calculado por meio do arquivo `grafico_ondaletas.py`. Para alterar quais períodos devem ser visualizados nos gráficos, é necessário ajustar os parâmetros relativos à análise de wavelet. Por padrão, ela foi configurada para trabalhar com dados horários `dt`.

## Leitura dos Dados de Ventos
A leitura é feita por meio do script `ler_dados.py`. Existem algumas funções relacionadas à leitura dos dados, como, por exemplo, a obtenção dos dados horários e o cálculo da média diária. O script pega os dados de ventos e já os formata em um DataFrame para facilitar o processo de manipulação. Por padrão, ele selecionará as 8 primeiras colunas dos dados.

## Gráficos das 7 Camadas dos Ventos

O script `plotar_colunas_ventos.py` realiza a plotagem das 7 camadas dos ventos para ambas as componentes.

## Dependências

Para executar os scripts acima, será necessário instalar algumas bibliotecas Python. Isso pode ser feito com o seguinte comando:

```pip install -r requirements.txt```
