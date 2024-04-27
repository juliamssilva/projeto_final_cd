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

#Função que recebe os parametos e faz as contas necessárias
def Antagonics(dataset1, dataset2, posicao1:str, posicao2: str):
    #selecionar apenas os valores númericos
    columns1 = dataset1.select_dtypes(include=['int', 'float']).columns
    columns2 = dataset2.select_dtypes(include=['int', 'float']).columns

    #Colocando os dados em uma lista
    num1 = dataset1[columns1].values.flatten().tolist()
    num2 = dataset2[columns2].values.flatten().tolist()

    #Transformando em matriz
    matriz = np.column_stack((num1,num2))

    df = pd.DataFrame(data=matriz, columns=['num1', 'num2'])

    GraphGrouping(matriz,2,df,num1,num2,posicao1,posicao2)

    

#Função que mostra o gráfico de agrupamento 
def GraphGrouping(matriz,num, data, c1, c2,p1,p2):

    kmeans = KMeans(n_clusters=num)

    kmeans.fit(matriz)

    centroids = kmeans.cluster_centers_

    labels = kmeans.labels_

    plt.figure(figsize=(8, 6))

    #PLotar os gráficos
    sns.scatterplot(data=data, x=c1, y=c2, hue=labels)

    plt.scatter(centroids[0, 0], centroids[0, 1], marker='^', s=200, c='blue', label='Centróides')
    plt.scatter(centroids[1, 0], centroids[1, 1], marker='^', s=200, c='orange', label='Centróides')


    plt.title("K-Means Clustering")
    plt.xlabel(f"{p1}")
    plt.ylabel(f"{p2}")
    plt.show()

#Função para os boxplots das habilidades por ano 
def BoxAttribbutes(dataset, posicao, habilidade):
    # Inicializar um DataFrame vazio
    dados_grafico = pd.DataFrame()

    for i in range(15, 25):
        # Copiar os dados filtrados
        filtred_data = dataset[(dataset["player_positions"].str.contains(posicao)) & (dataset["fifa_version"] == i)].copy()

        # Adicionar a coluna "fifa_version" com o valor atual
        filtred_data["fifa_version"] = i

        # Verificar se é a primeira iteração
        if dados_grafico.empty:
            dados_grafico = filtred_data
        else:
            # Concatenar os dados
            dados_grafico = pd.concat([dados_grafico, filtred_data])

    # Plotar o boxplot
    plt.figure(figsize=(14, 7))
    sns.boxplot(data=dados_grafico, x="fifa_version", y=habilidade)
    plt.title(f"Boxplot da {habilidade} dos {posicao} em Todas as Versões do FIFA")
    plt.xlabel("Versão do FIFA")
    plt.ylabel(f"{habilidade}")
    plt.ylim(0, 150)
    plt.show()
