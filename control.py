import matplotlib.pyplot as plt
import ler_dados as ler
import pandas as pd
from numpy import (sin, cos, pi, sqrt, arange, array, mean, sum as sm)
from scipy.optimize import curve_fit as cv

# Define uma função para calcular um senoide dado um tempo
def func_seno(tempo):
    periodo = 2 
    senoide = sin(2*pi*tempo/(1*periodo))
    return senoide

# Define uma função para calcular um cosseno dado um tempo
def func_cosseno(tempo):
    periodo = 2
    cosseno = cos(2*pi*tempo/(1*periodo))
    return cosseno

# Define uma função para realizar um ajuste linear combinando seno e cosseno
def ajuste(tempo, A, B):
    funcao = A*func_cosseno(tempo)+B*func_seno(tempo)
    return funcao

# Define uma função para calcular a amplitude do sinal
def calc_amp(sinal, tempo, max_calc):
    coefi, estatistico= cv(ajuste, tempo, sinal, p0=(1, 1), maxfev=max_calc)
    R = sqrt((coefi[0]**2)+(coefi[1]**2))
    return coefi[0], coefi[1], R

# Define uma função para aplicar uma janela móvel nos dados
def janela_movel(sinal, tempo, periodo):
    dados = []
    if periodo == 1:
        janela = periodo * 3 *24
    elif periodo == 2:
        janela = periodo * 5 * 24
    else:
        janela = periodo*30
    fim = len(sinal) - janela
    for i in arange(0, fim):
        sinal_j = sinal.iloc[i:janela + i]
        tempo_j = tempo.iloc[i:janela + i]
        parametros = calc_amp(sinal=sinal_j, tempo=tempo_j, max_calc=2000)
        dados.append(parametros)
    return pd.DataFrame(dados, columns=['a', 'b', 'r'])

if __name__=='__main__':
    # Configurações iniciais
    
    periodo = 2
    tamanho = 24*60+periodo*5*24
    # Lê os dados brutos
    dados = ler.ler_bruto('ventos/Cachoeira/wind.200601-200608.brazil.mer').iloc[0:tamanho]
    colunas = ler.colunas
    tempo = pd.Series(dados.index)
    
    # Configura a figura para os gráficos
    fig, axs = plt.subplots(len(colunas) - 1, figsize=(10, 8*len(colunas) - 1))
    
    # Itera sobre as colunas e gera os gráficos de ajuste
    for i, coluna in enumerate(colunas[1:]):
        sinal = dados[coluna]
        sinal.interpolate(method='linear', inplace=True)
        ajuste_df = janela_movel(sinal, tempo, periodo)
        axs[i].plot(ajuste_df)
        axs[i].set_title(f'{coluna}', fontsize=12, fontweight='bold')
        axs[i].tick_params(axis='both', which='both', labelsize=12)
    
    # Adiciona título à figura e exibe os gráficos
    fig.suptitle('Gráficos de Ajuste', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
