import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from pathlib import Path
from waveletFunctions import wave_signif, wavelet
import ler_dados as ler
from datetime import datetime, timedelta

caminho = Path('ventos')
arquivos = sorted([str(i) for i in caminho.glob('**/wind*') if str(i).endswith('.mer') or str(i).endswith('.zon')])

# Função para criar um array de datas entre duas datas específicas, variando de 5 em 5 dias
def daterange(start_date, end_date):
    delta = timedelta(days=5)
    while start_date < end_date:
        yield start_date
        start_date += delta

# Definindo a data de início e fim
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 2, 29)  # Assumindo ano bissexto

# Lista de datas entre start_date e end_date
dates = []
for date in daterange(start_date, end_date):
    dates.append(date.strftime("%d - %b"))

# Número de pontos de data deve ser igual ao número de pontos de dados
num_points = len(dates)

# Loop sobre cada arquivo na lista de arquivos
for arquivo in arquivos:
    # Leitura dos dados do arquivo
    dados = ler.ler_bruto(arquivo)
    info_arquivo = ler.cidade_componentes(arquivo)

    def daterange(start_date, end_date):
        delta = timedelta(days=5)
        while start_date < end_date:
            yield start_date
            start_date += delta

    # Definindo a data de início e fim
    ano = int(info_arquivo[1][:-2])
    start_date = datetime(ano, 1, 1)
    end_date = datetime(ano, 3, 1)  # Assumindo ano bissexto

    # Lista de datas entre start_date e end_date
    dates = []
    for date in daterange(start_date, end_date):
        dates.append(date.strftime("%d - %b"))

    # Número de pontos de data deve ser igual ao número de pontos de dados
    num_points = len(dates)
    # Criação da figura e grid de subplots
    fig = plt.figure(figsize=(9, 12))
    if info_arquivo[0] == 'Cariri':
        fig.suptitle(f"Espectro de Potência para São João do {info_arquivo[0]} Ano de {info_arquivo[1][:-2]}-{info_arquivo[-1]}", y=0.95, fontsize=14, weight='bold')  # Ajuste para posicionar o título principal um pouco mais próximo dos subplots
    else:
        fig.suptitle(f"Espectro de Potência para {info_arquivo[0]} Paulista Ano de {info_arquivo[1][:-2]}-{info_arquivo[-1]}", y=0.95, fontsize=14, weight='bold')  # Ajuste para posicionar o título principal um pouco mais próximo dos subplots
    
    gs = GridSpec(3, 2, height_ratios=[1, 1, 1], hspace=0.19, wspace=0.11)  # Ajuste do espaçamento vertical entre subplots

    # Loop sobre as colunas de interesse nos dados
    for pos, coluna in enumerate(ler.colunas[1:-1]):
        print(coluna)
        if pos<3:
            plt3 = plt.subplot(gs[pos, 0])
        else:
            plt3 = plt.subplot(gs[pos-3, 1])
        plt3.set_title(f"Altitude {coluna}", fontsize=12, weight='bold')  # Adicionando título em negrito e aumentando o tamanho da fonte
        # Adicionando label em negrito e aumentando o tamanho da fonte
        
        # Adicionando um pequeno espaço entre o título e o eixo y
        plt3.title.set_position([0.5, 0.9])

        sst = dados[coluna].iloc[0:24*60]
        time = np.arange(1, len(sst)+1)

        sst.interpolate(method='linear', inplace=True)
        sst = sst  - np.mean(sst)
        variance = np.std(sst, ddof=1) ** 2

        n = len(sst)
        dt = 1.083 - 1.042 
        time = np.arange(sst.shape[0])
        pad = 1
        dj = 0.01
        s0 = 7*dt
        j1 = 4/ dj
        lag1 = 0.72
        mother = 'MORLET'

        wave, period, scale, coi = wavelet(sst, dt, pad, dj, s0, j1, mother)
        power = (np.abs(wave)) ** 2
        global_ws = (np.sum(power, axis=1) / n)
        signif = wave_signif(([variance]), dt=dt, sigtest=0, scale=scale,
            lag1=lag1, mother=mother)
        sig95 = signif[:, np.newaxis].dot(np.ones(n)[np.newaxis, :])
        sig95 = power / sig95

        dof = n - scale
        global_signif = wave_signif(variance, dt=dt, scale=scale, sigtest=1,
            lag1=lag1, dof=dof, mother=mother)

        avg = np.logical_and(scale >= 2, scale < 8)
        Cdelta = 0.776
        scale_avg = scale[:, np.newaxis].dot(np.ones(n)[np.newaxis, :])
        scale_avg = power / scale_avg
        scale_avg = dj * dt / Cdelta * sum(scale_avg[avg, :])
        scaleavg_signif = wave_signif(variance, dt=dt, scale=scale, sigtest=2,
            lag1=lag1, dof=([2, 7.9]), mother=mother)

        cs = plt3.contourf(np.linspace(0, num_points-1, len(time)), period, power, cmap='cividis')
        #plt.colorbar(cs)
        im = plt3.contour(np.linspace(0, num_points-1, len(time)), period, power, cmap='cividis')
        plt3.contour(np.linspace(0, num_points-1, len(time)), period, sig95, [-99, 1], colors='k')
        plt.fill_between(np.linspace(0, num_points-1, len(time)), coi * 0 + period[-1], coi, facecolor="none",edgecolor="#00000040", hatch='x')
        plt.plot(np.linspace(0, num_points-1, len(time)), coi, 'k')

        plt3.set_xticks(np.arange(0, num_points))
        plt3.set_xticklabels(dates, rotation=45)  # Rotacionar as datas para melhor visualização

        plt3.set_yscale('log', base=2, subs=None)
        plt.ylim([np.min(period), np.max(period)])
        ax = plt.gca().yaxis
        ax.set_major_formatter(ticker.ScalarFormatter())
        plt3.ticklabel_format(axis='y', style='plain')
        plt3.invert_yaxis()
        # Removendo o eixo x dos dois primeiros subplots
        if pos == 2 or pos == 5:
            plt3.set_xlabel('Tempo', fontsize=12, weight='bold')  # Adicionando título do eixo x em negrito e aumentando o tamanho da fonte
        else:
            plt3.set_xticks([])
        if pos < 3:
            plt3.set_ylabel('Período', fontsize=12, weight='bold')  
        else:
            plt3.set_yticks([])


    # Exibição da figura
    fig.savefig(f'figuras/{info_arquivo[0]}_{info_arquivo[1][:-2]}_{info_arquivo[-1]}.png')
