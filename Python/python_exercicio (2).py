# ====================================//=====================================
#                     Exercício Python para Ciência de Dados
# ===================================//======================================

# Carregar o arquivo .csv (arquivo com os dados, em formato csv, planilha)
from datetime import date # importações automáticas
from numpy import datetime64, dtype # VScode importa funções automaticamente
import pandas #importando a biblioteca pandas
data = pandas.read_csv ('Projeto_DS_1/datasets/kc_house_data.csv') # lê o arquivo com o comando read da pandas e guarda na variável data.


# 1. Quantas casas estão disponíveis para compra?
# R: Total de linhas, 21613.
# print(data.shape)

# # 2. Quantos atributos as casas possuem?
# R: Total de colunas, 21.
# print(data.shape)

# # 3. Quais são os atributos das casas?
# R: atributos das colunas
#print(data.columns)

# # 4. Qual a casa mais cara ( casa com o maior valor de venda)?
# R: id: 6762700020; Preço:  7700000.0
# print(data[['id','price']].sort_values('price', ascending=False))

# # 5. Qual a casa com o maior número de quartos?
# R: id: 2402100895; Quartos: 33
# print(data[['id','bedrooms']].sort_values('bedrooms', ascending=False))

# # 6. Qual a soma total de quartos do conjunto de dados?
# R: 72854
# print(data['bedrooms'].sum())

# 7. Quantas casas possuem 2 banheiros?
# R: várias maneiras, 1930
# 1.
# print(data[data['bathrooms'] == 2].shape)
# # 2.
#print(data['bathrooms'].loc[data['bathrooms'] == 2])
# # 3.
# print(data['bathrooms'].loc[data['bathrooms'] == 2].shape)

# 8. Qual o preço médio de todas as casas no conjunto de dados?
# R: 540088.14...
#print(data['price'].mean())

# 9. Qual o preço médio de casas com 2 banheiros?
# R:
#print(data[data['bathrooms'] == 2]['price'].mean())

# 10. Qual o preço mínimo entre as casas com 3 quartos?
# R:
#print(data[data['bedrooms'] == 3]['price'].min())

# 11. Quantas casas possuem mais de 300 metros quadrados na sala de estar?
# R: 21612
#print(data[data['sqft_living'] > 300].shape)

# 12. Quantas casas tem mais de 2 andares?
# R: 782
#print(data[data['floors'] > 2].shape)

# 13. Quantas casas tem vista para o mar?
# R: 163
#print(data['waterfront'].unique()) ###### retorna os valores possíveis e existentes na coluna

#print(data[data['waterfront'] == True].shape)
# ou 
#print(data[data['waterfront'] == 1].shape)


# 14. Das casas com vista para o mar, quantas tem 3 quartos?
# R: 64

#print(data.loc[(data['waterfront'] == 1) & (data['bedrooms'] == 3)].shape) ###### com função loc não aparece mensagem de aviso
# ou
#print(data[data['bedrooms'] == 3][data['waterfront'] == 1].shape) ###### com mensagem de aviso

# 15. Das casas com mais de 300 metros quadrados de sala de estar, quantas tem mais de 2 banheiros?
# R: 11242
#print(data.loc[(data['sqft_living'] > 300) & (data['bathrooms'] > 2)].shape)


#1. Qual a data do imóvel mais antigo no portfólio?
# R: 2014-05-02
#data['date'] = pandas.to_datetime(data['date'])
#print(data[['id', 'date']].sort_values('date', ascending=True))


#2. Quantos imóveis possuem o número máximo de andares (3.5)?
# R: 8
#print(data['floors'].unique())  ###### o máximo é 3.5
#print(data[data['floors'] == 3.5].shape)


#3. Criar uma classificação para os imóveis, separando-os em baixo e alto padrão de acordo com o preço
# -acima de R$ 540.000, alto padrão 'high_lvl'
# -abaixo de R$ 540.000, baixo padrão 'low_lvl'
# -igual a R$ 540.000, padrão médio 'average_lvl'
# R:
# data['level'] = 'Undef'  ###### cria a coluna level (nível/classificação)
# data.loc[data['price'] > 540000, 'level'] = 'high_level' ###### .loc é usado quando se que mostrar uma coluna especificada , não todas, que no caso é a coluna "level".
# data.loc[data['price'] < 540000, 'level'] = 'low_level'
# data.loc[data['price'] == 540000, 'level'] = 'average_lvl'

##print(data['level'].unique())
##print(data[['level', 'price']].loc[data['level'] == "Undef"]) #ou #print(data.loc[data['level'] == "Undef", ['id', 'level', 'price']])
##print(data.loc[data['level'] == "Undef"])


#4. Criar um relatório ordenado pelo preço e contendo as seguintes informações:
# id do imóvel, data que o imóvel ficou disponível para compra, o numero de quartos, o tamanho total do terreno, o preço a classificação (alto e baixo padrão)

# colsrepo = ['id', 'date', 'bedrooms', 'sqft_lot', 'price', 'level']
# report = data[colsrepo].sort_values('price', ascending=False)
# report.to_csv('Projeto_DS_1/datasets/report.csv', index=False) ###### IMPORTANTE: o parâmetro "index=false" serve para resetar o index antes de salvar, pois quando ausente, o arquivo será salvo com os index originais. Com os index originais, quando for ler novamente, o conteúdo vai estar desorganizado.  to_csv serve para salvar como csv o conteúdo da variável "report", que é uma planilha. Entre parênteses deve ser indicado o caminho para salvar. 


#5. Criar um mapa indicando onde as casas estão localizadas geograficamente.
# -> Plotly, matplotlib, folium - Bibliotecas que armazena a função que desenha mapa
# -> scatter_mapBox - função de desenha um mapa

# import plotly.express

# data_mapa = data[['id', 'lat', 'long', 'price']]

# mapa = plotly.express.scatter_mapbox( data_mapa, 
#                          lat='lat', 
#                          lon='long', 
#                          hover_name='id',
#                          hover_data=['price'],
#                          color_discrete_sequence=['crimson'],
#                          zoom=8 ,
#                          height=300)

# mapa.update_layout(mapbox_style='open-street-map')
# mapa.update_layout(height=600, margin={'r':0, 't':0, 'l':0, 'b':0})

# mapa.show()

# mapa.write_html('Projeto_DS_1/datasets/mapa_casas.html')
