# Importação das bibliotecas necessárias
import matplotlib.pyplot as plt
import matplotlib as mpl
import ler_dados as ler
from pathlib import Path as pt
import numpy as np

# Definindo o estilo padrão da fonte para negrito
mpl.rcParams['font.weight'] = 'bold'

# Definição do caminho para os arquivos de dados
caminho = pt('ventos')

# Lista de arquivos na pasta 'Cariri' com nomes que terminam com '.mer' ou '.zon'
arquivoscar = sorted([str(i) for i in caminho.glob('Cariri/**/mean*') if str(i).endswith('.mer') or str(i).endswith('.zon')])

# Iteração sobre os arquivos do Cariri
for cari in arquivoscar:
    # Obtendo os componentes do nome da cidade do arquivo
    nome_cariri_componente = ler.cidade_componentes(cari)
    # Lendo os dados brutos do arquivo
    sinal_cari = ler.ler_bruto(cari)
    # Criando o vetor de tempo para os dados do Cariri
    tempo_cari = np.arange(1, len(sinal_cari)+1)
    # Criando a figura e os eixos para plotagem
    fig, ax = plt.subplots(7, figsize=(7, 7))
    # Título da figura com o nome da cidade, componente e altitude
    fig.suptitle(nome_cariri_componente[0]+'-'+nome_cariri_componente[3]+'-'+nome_cariri_componente[2][:-2], fontweight='bold')
    # Espessura da linha reduzida conforme especificado
    larg = 0.6
    # Índice vertical inicial para a iteração
    vertical = 6
    # Iteração sobre as 7 primeiras colunas de sinal_cari
    for i, e in enumerate(sinal_cari.columns[:7]):
        # Selecionando os dados para o componente atual
        dados_cari = sinal_cari[e][:366]  # Limitando aos primeiros 366 dias
        # Configurando os eixos y para não exibir rótulos
        ax[vertical-i].set_yticklabels([''], fontweight='bold')
        ax[vertical-i].set_yticks([])  # Removendo as marcas do eixo y
        # Definindo o rótulo do eixo y com o nome do componente
        ax[vertical-i].set_ylabel(e, fontweight='bold')
        # Plotando os dados do componente atual
        ax[vertical-i].plot(dados_cari, linewidth=larg, color='k')  # Plot em preto com a espessura definida
        ax[vertical-i].set_xlim(left=0.5)  # Define o limite esquerdo para 0.5
        ax[vertical-i].set_xlim(right=len(dados_cari))  # Define o limite direito para 365.5
        ax[i].set_xlabel('Período em dias', fontweight='bold')  # Rótulo do eixo x para todos os subplots

    plt.tight_layout()  # Ajusta o layout da figura
    plt.subplots_adjust(hspace=0.09)  # Ajusta o espaçamento vertical entre os subplots

    plt.show()  # Mostra a figura
