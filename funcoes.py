#Todas as funções usadas no projeto 

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans


#Função para pegar os 500 melhores atributos por ano
def ComparePlayers(posicao: str, dataset, atribute: str):
    all_players_data = [] 
    for i in range(15, 25):
        area = dataset[(dataset["player_positions"].str.contains(posicao)) & 
                       (dataset["fifa_version"] == i) & 
                       (dataset[atribute])]

        #Selecionando os 500 maiores atributos
        #O sorted organiza em ordem descrescente e o iloc[:500] pega as primeiras 500 linhas          
        players = sorted(area[atribute].iloc[:500], reverse=True) 
        all_players_data.append(players)
    
    dfr = pd.DataFrame(all_players_data, index=[f"FIFA_{i}" for i in range(15, 25)])
    return dfr



# Gráfico de linha
def PlotLineGraph(dataset, attribute: str):
    
    # Transformando as linhas em coluna e vice-versa para facilitar o cálculo da média
    correcao_dataset = dataset.T

    # Calculando a média da coluna, que no caso são os anos
    mean = dataset.T.mean()

    # Tamanho da figura
    plt.figure(figsize=(10, 6))

    plt.plot(mean.index, mean, marker='o')
    plt.title(f"Média dos Melhores 500 {attribute} por Ano")
    plt.xlabel("Ano")
    plt.ylabel("Média por Ano")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#ok