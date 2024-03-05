import pandas as pd
from pathlib import Path as pt
import re


def cidade_componentes(nome_do_arquivo):
    padrao = r'\b(?:Cariri|Cachoeira|zon|mer)|\d{6}\b'
    busca = re.findall(padrao, nome_do_arquivo)
    return busca


def ler_dados_covert_me(arquivo):


    """    
    O programa recebe o nome do arquivo a ser trabalhado e a leitura é realizada pela
    biblioteca pandas. As colunas dos dados são definidas na variável 'colunas'. O
    intervalo começa na coluna inicial e vai até a coluna final, pulando de 3 em 3, já
    que as altitudes são espaçadas de 3 em 3 km.

    Na variável 'data', é feita a leitura do arquivo fornecido, aplicando algumas
    condições durante a leitura.
    Primeira condição: o programa ignora a primeira e terceira linha do arquivo, 
    pois contêm apenas informações sobre o tipo de dados.

    Segunda condição: são definidas as colunas que serão utilizadas ao carregar o
    arquivo. As colunas originais do arquivo apresentam um problema na importação,
    necessitando de uma nova nomenclatura.

    O programa retorna o arquivo já com as devidas correções da estrutura e a media
    diárias dos ventos calculadas, já que os dados de origem são de hora em hora.

    """
    colunas = [f"alt{i}-km" for i in range(81, 102, 3)]
    colunas.insert(0, 'tempo')

    global data

    data = pd.read_fwf(arquivo, skiprows=[0, 2], usecols=[0, 1, 2, 3, 4, 5, 6, 7])
    data.columns = colunas
    medias = data.groupby(data.index//24).mean()
    medias.set_index('tempo', inplace=True)
    return pd.DataFrame(medias)
     

def func_all_arquivos(pasta='ventos'):

    """
    
    Utilize esta função no caso de estar trabalhando com muitos arquivos em várias
    pastas. Forneça uma pasta inicial e o programa fará uma varredura recursiva
    dentro das pastas, procurando pelos arquivos com as extensões fornecidas. Útil
    para automatizar processos com múltiplas bases de dados.

    Seleciona os arquivos com extensão .mer e .zon dentro das pastas encontradas.

    A variável 'arquivos' é uma lista com todos os nomes dos arquivos
    encontrados. Será a váriavel de retorno da função.
    
    """

    cam = pt(pasta)
    arquivos = [str(i) for i in cam.glob('**/wind*') if str(i).endswith('.mer') or str(i).endswith('.zon')]
    return arquivos


def ler_bruto(arquivo):
    """
    Apenas ler o arquivo por meio de uma limpeza básica e organiza os valores em colunas nomeadas

    """
    global colunas
    colunas = [f"{i}km" for i in range(81, 102, 3)]
    colunas.insert(0, 'tempo')

    data = pd.read_fwf(arquivo, skiprows=[0, 2], usecols=[0, 1, 2, 3, 4, 5, 6, 7])
    data.columns = colunas
    data.set_index('tempo', inplace=True)
    return data



if __name__ == "__main__":
    print(ler_bruto('ventos/Cariri/wind.200601-200612.cariri.zon'))