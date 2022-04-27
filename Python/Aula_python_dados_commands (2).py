# ====================================//=====================================
#                     Aula de python para Ciência de Dados
# ===================================//======================================

# Carregar o arquivo .csv (arquivo com os dados, em formato csv, planilha)
from datetime import date # importações automáticas
from numpy import datetime64, dtype # VScode importa funções automaticamente
import pandas #importando a biblioteca pandas
data = pandas.read_csv ('Workspace/Data Science/Projeto_DS_1/datasets/kc_house_data.csv') # lê o arquivo com o comando read da pandas e guarda na variável data.


# ====================================//=====================================
#                          Primeiros comandos úteis
# ===================================//======================================

# mostrar as 5 primeiras linhas da planilha
#print(data.head())

# mostrar a quantidade de linhas e colunas do arquivo
#print(data.shape)

# mostrar o nome das colunas do arquivo
#print(data.columns)

# mostrar o conjunto de dados do arquivo, ordenados pela coluna 'price'
#print(data[['id','price']].sort_values('price'))

# mostrar o conjunto de dados do arquivo, ordenados pela coluna 'price' do maior ao menor
#print(data[['id','price']].sort_values('price', ascending=False))

# mostrar o conjunto de dados do arquivo, ordenados pela coluna 'bedrooms' do maior ao menor
#print(data[['id','bedrooms']].sort_values('bedrooms', ascending=False))

# função que converte de "object" (string) para "date" (pois a pandas reconhece datas como objetos por padrão)
#data['date'] = pandas.to_datetime(data['date'])
 
# mostrar os tipos de variaveis em cada coluna
#print(data.dtypes)

# retorna/mostra uma lista com os valores possíveis e existentes na coluna.
#print(data['bedrooms'].unique())

# ====================================//=====================================
#                     Converter o tipo de uma variável
# ===================================//======================================

# 1. object -> date  (igual ao 6)
#data['date'] = data['date'].astype(datetime64)

# 2. integer -> float
#data['bedrooms'] = data['bedrooms'].astype(float)

# 3. float -> integer                                   ###### Note: int64 significa que os tipos das variáveis estão, e devem estar, em 64 bits. Caso seja 32 bits (int32, float32), todos devem ser em 32 bits, pois 64 e 32 não são comparáveis.
#data['bedrooms'] = data['bedrooms'].astype(int64)

# 4. integer -> string                                  ###### Note: strings são considerados obejcts.     
#data['bedrooms'] = data['bedrooms'].astype(str)

# 5. string -> integer
#data['bedrooms'] = data['bedrooms'].astype(int64)

# 6. string -> date
#data['date'] = pandas.to_datetime(data['date'])

#print(data.dtypes)

#print(data.head())

# ====================================//=====================================
#                          Manipulando variáveis 
# ===================================//======================================

# 1. Criar

## utiliza-se o operador "=" (igual) para atribuir valor a uma variável.

### Ex: 
#data = pandas.read_csv ('Projeto_DS_1/datasets/kc_house_data.csv') ###### Leu o arquivo e guardou-o na variável "data".


### Ex2: criando colunas na planilha de dados do arquivo
#data['meu_nome'] = "Paulo"
#data['Idade'] = 27
#data['Data_de_Nascimento'] = pandas.to_datetime('1995-10-25') ###### pode-se converter de object para date depois, ou converter no ato, como no exemplo.


### Ex3: criando variável contendo uma lista
#col_creat = ['meu_nome', 'Idade', 'Data_de_Nascimento'] ###### cria a lista ... e armazena ela na variável col_creat

#print(data[['id','date', 'meu_nome', 'Idade', 'Data_de_Nascimento']].head()) ###### Note: mostra as colunas indicadas (id, date, meu_nome...)
#print(data.dtypes) 
#print(data.columns) ###### APENAS PARA VISUALIZAÇÃO!!!!!


# ===================================//======================================

# 2. Deletar

## utiliza-se "drop" para apagar. Essa função exige um eixo (axis), que significa apagar em direção às colunas, ou em direção às linhas.

### Ex:
#print(data.columns)

#data = data.drop(['meu_nome', 'Idade', 'Data_de_Nascimento'], axis=1) ###### Note: é necessário atribuir novamente o valor à variável data, após apagar as colunas, por isso o "data =" no começo. Também é possível atribuir a uma nova planilha "data2 =".

#print(data.columns) ###### APENAS PARA VISUALIZAÇÃO!!!!!


# ===================================//======================================

# 3. Selecionar

# 3.1 Selecionar pelo nome das colunas

### Ex:
#print(data[['id','price', 'bedrooms']]) ###### Note: "print" serve apenas para mostrar o resultado.

### ou

#cols = ['id','price', 'bedrooms'] ###### criar variável com lista antes.
#print(data[cols]) ###### selecionar a lista.

#____________________________________________________________________________
# 3.2 Selecionar pelos índices (index) das linhas e das colunas

## forma -> iloc[intervalo de linhas, intervalo de colunas]

### Ex:
#print(data.iloc[0:5, 0:3])

#____________________________________________________________________________
# 3.3 Selecionar pelos índices das linhas e pelo nome das colunas

## forma -> loc[intervalo de linhas, nome da coluna/lista]

### Ex:
#print(data.loc[0:4, ['id','price', 'bedrooms']])

### ou

#cols = ['id','price', 'bedrooms']
#print(data.loc[0:4, cols])

#____________________________________________________________________________
# 3.4 Selecionar pelos índices booleanos (True, False)

## forma -> precisa ser uma lista de True e False, na mesma quantidade de colunas.

### Ex:
#cols = [True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False ]
#print(data.loc[0:4, cols])
