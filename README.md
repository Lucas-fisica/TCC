# TCC

# Uso das Funções do aruivo control.py

Este arquivo README fornece uma explicação sobre o uso de cada função no script Python fornecido.

## Funcões e Descrições

### func_seno(tempo)

Esta função calcula a função seno para um dado tempo.

**Parâmetros:**
- tempo: Um array ou lista contendo valores de tempo.

**Resultado Esperado:**
A função retornará um array ou lista com os valores da função seno correspondentes ao tempo fornecido.

### func_cosseno(tempo)

Esta função calcula a função cosseno para um dado tempo.

**Parâmetros:**
- tempo: Um array ou lista contendo valores de tempo.

**Resultado Esperado:**
A função retornará um array ou lista com os valores da função cosseno correspondentes ao tempo fornecido.

### ajuste(tempo, A, B)

Esta função realiza um ajuste de curva utilizando uma combinação linear de seno e cosseno.

**Parâmetros:**
- tempo: Um array ou lista contendo valores de tempo.
- A: Coeficiente que multiplica a função cosseno.
- B: Coeficiente que multiplica a função seno.

**Resultado Esperado:**
A função retornará um array ou lista contendo os valores ajustados correspondentes ao tempo fornecido e aos coeficientes dados.

### coeficientes(sinal, tempo, periodo)

Esta função calcula os coeficientes de ajuste (A e B) e o coeficiente de correlação (R) para um sinal dado.

**Parâmetros:**
- sinal: Um array ou lista contendo os valores do sinal.
- tempo: Um array ou lista contendo valores de tempo.
- periodo: O período do sinal.

**Resultado Esperado:**
A função retornará os coeficientes A e B e o coeficiente de correlação R.

### calc_amp(sinal, tempo, max_calc)

Esta função calcula a amplitude de um sinal utilizando o método de ajuste de curva.

**Parâmetros:**
- sinal: Um array ou lista contendo os valores do sinal.
- tempo: Um array ou lista contendo valores de tempo.
- max_calc: O número máximo de cálculos permitidos.

**Resultado Esperado:**
A função retornará a amplitude do sinal.

### janela_movel(sinal, tempo, periodo)

Esta função cria janelas móveis e calcula os coeficientes de ajuste para cada janela.

**Parâmetros:**
- sinal: Um array ou lista contendo os valores do sinal.
- tempo: Um array ou lista contendo valores de tempo.
- periodo: O período do sinal.

**Resultado Esperado:**
A função retornará um DataFrame contendo os coeficientes A e B e o coeficiente de correlação R para cada janela móvel.

## Como Usar

Para utilizar essas funções, você precisa importar o script Python e chamar cada função conforme necessário, fornecendo os parâmetros corretos. Consulte a descrição de cada função para obter detalhes sobre os parâmetros necessários e os resultados esperados.
