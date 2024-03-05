import control as ct
import matplotlib.pyplot as plt
import ler_dados as ler
import pathlib as pt
import numpy as np

# Definição do caminho onde os arquivos estão localizados
caminho = pt.Path('ventos')

# Listagem dos arquivos no caminho especificado
arquivos = sorted([str(i) for i in caminho.glob('**/wind*') if str(i).endswith('.mer') or str(i).endswith('.zon')])

# Períodos de interesse
periodos = [2]

# Iteração sobre os períodos
for periodo in periodos:
    # Criação de duas figuras contendo 2x2 subplots cada
    fig1, ax1 = plt.subplots(2, 2, figsize=(14, 12))
    fig2, ax2 = plt.subplots(2, 2, figsize=(14, 12))
    
    # Título principal para a figura 2
    fig2.suptitle('Cachoeira Paulista', fontsize=18, fontweight='bold')
    
    # Título principal para a figura 1
    fig1.suptitle('São João do Cariri', fontsize=18, fontweight='bold')
    
    # Ajuste de espaçamento entre os subplots
    fig1.subplots_adjust(wspace=0.1, hspace=0.3)
    fig2.subplots_adjust(wspace=0.1, hspace=0.3)
    
    # Contadores de posição para os subplots
    pos1 = 0
    pos2 = 0
    pos1_2 = 0
    pos2_2 = 0
    
    # Iteração sobre os arquivos
    tamanho = 24*60+periodo*5*24
    for arquivo in arquivos:
        
        # Leitura dos dados brutos do arquivo
        dados = ler.ler_bruto(arquivo).iloc[0: tamanho]
        
        # Colunas dos dados
        colunas = ler.colunas[1:]
        
        # Informações sobre o arquivo
        info_arquivo = ler.cidade_componentes(arquivo)
        print(info_arquivo)
        # DataFrames vazios para armazenar amplitudes e fases
        amplitudes = ler.pd.DataFrame([], columns=colunas)
        
        # Série temporal
        tempo = ct.pd.Series(dados.index)
        
        # Loop sobre as colunas
        for coluna in colunas:
            # Sinal da coluna atual
            sinal = dados[coluna]

            sinal = sinal.interpolate(method='linear')
            sinal = sinal.fillna(np.mean(sinal))
            # Cálculo das amplitudes e fases usando janelas móveis
            parametros = ct.janela_movel(sinal, tempo, periodo)
            amplitudes[coluna] = parametros['r']

        # Transposição das amplitudes para obter as altitudes como índice
        z = amplitudes.T
 

        # Verificação do local (Cariri ou Cachoeira) e tipo de arquivo (mer ou zon) para plotagem
        if info_arquivo[0] == "Cariri":
            if info_arquivo[-1] =='mer':
                # Plotagem do contorno para os dados
                bar1 = ax1[pos1, 0].contourf(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                fig1.colorbar(mappable=bar1, ax=ax1[pos1, 0]).set_label('m/s', fontsize=12, fontweight='bold')
                ax1[pos1, 0].contour(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                ax1[pos1, 0].set_title(f'{info_arquivo[1][:-2]} - Amp da onda de {periodo} - meridional', fontsize=12, fontweight='bold')
                pos1 += 1
            else:
                bar1 = ax1[pos1_2, 1].contourf(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                fig1.colorbar(mappable=bar1, ax=ax1[pos1_2, 1]).set_label('m/s', fontsize=12, fontweight='bold')
                ax1[pos1_2, 1].contour(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                ax1[pos1_2, 1].set_title(f'{info_arquivo[1][:-2]} - Amp da onda de {periodo} - zonal', fontsize=12, fontweight='bold')
                pos1_2 += 1
        elif info_arquivo[0] == "Cachoeira":
            if info_arquivo[-1] == 'mer':
                bar2 = ax2[pos2, 0].contourf(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                fig2.colorbar(mappable=bar2, ax=ax2[pos2, 0]).set_label('m/s', fontsize=12, fontweight='bold')
                ax2[pos2, 0].contour(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                ax2[pos2, 0].set_title(f'{info_arquivo[1][:-2]} - {info_arquivo[-1]} - Amp da onda de {periodo} - meridional', fontsize=12, fontweight='bold')
                pos2 +=1
            else:
                bar2 = ax2[pos2_2, 1].contourf(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                fig2.colorbar(mappable=bar2, ax=ax2[pos2_2, 1]).set_label('m/s', fontsize=12, fontweight='bold')
                ax2[pos2_2, 1].contour(tempo.iloc[:z.shape[1]], colunas, z, cmap='cividis')
                ax2[pos2_2, 1].set_title(f'{info_arquivo[1][:-2]} - Amp da onda de {periodo} - zonal', fontsize=12, fontweight='bold')
                pos2_2 += 1

# Salvando as figuras
fig1.savefig('figuras/cariri_amplitude.png')
fig2.savefig('figuras/cachoeira_amplitude.png')
