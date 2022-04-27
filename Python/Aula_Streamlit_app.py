#===================================================================
                               # Aula Streamlit #
#===================================================================
from datetime import datetime
from turtle import fillcolor
import pandas as pd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True) # decorador, ou seja, ele lê diretamente da memória ram (cache). "True" significa que é mutável
def get_data(path):
    data = pd.read_csv(path)
    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile


#get data
path = 'datasets/kc_house_data.csv'
data = get_data(path)

# get geofile
url ='https://opendata.arcgis.com/api/v3/datasets/83fc2e72903343aabff6de8cb445b81c_2/downloads/data?format=geojson&spatialRefId=4326'
geofile = get_geofile(url)

# adicionando colunas (features)
data['price_m^2'] = data['price'] / data['sqft_lot']

data['date'] = pd.to_datetime(data['date'])


#=======================================================================
#data overview (visão geral dos dados)
#=======================================================================

# Filtros para a barra lateral
## Quando attributes + zipcode ativos no app: irá selecionar colunas e linhas específicadas
## Somente attributes: seleciona as colunas especificadas
## Somente zipcode: seleciona as linhas especificadas
## nenhuma opção de filtro selecionada: retornará o dataset original

f_attributes = st.sidebar.multiselect('Enter columns', data.columns) # filtro para as colunas

f_zipcode = st.sidebar.multiselect(
    'Enter zipcode', 
    data['zipcode'].unique()) # filtra as linhas pelo número do zipcode. unique() verifica todos os valores de zipcode que existem nas linhas

if (f_zipcode != []) & (f_attributes != []): # significa que um filtro por zipcode e um filtro por coluna estão selecionados. ## "!= []" (diferente de vazio), está selecionado;
    data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes] 

elif (f_zipcode != []) & (f_attributes == []): # ## "== []" (igual a vazio), não está selecionado.
    data = data.loc[data['zipcode'].isin(f_zipcode), :] # o termo ":" significa que todas as colunas serão mostradas (selecionadas)

elif (f_zipcode == []) & (f_attributes != []): 
    data = data.loc[:, f_attributes] # # o termo ":" significa que todas as linhas serão mostradas.

else:
    data = data.copy()

st.title('Metrics and Stats')
st.header('Data')
st.write(data)

c1, c2 = st.columns((1, 1)) # Ajusta a disposição dos gráficos

# ###########        Métricas           #################
## Número de casas, por região (zipcode)
df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()

# ## Média de preço por região
df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

# ## média da sala de estar por região
df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()

# ## média de preços por metro quadrado, por região
df4 = data[['price_m^2', 'zipcode']].groupby('zipcode').mean().reset_index()

## Merge: junta dois dataframes, com opção de escolher a coluna em comum ('zipcode', no caso)
m1 = pd.merge(df1, df2, on='zipcode', how='inner') # só pode juntar dois dataframes por vez
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
df = pd.merge(m2, df4, on='zipcode', how='inner') 

# Renomeando as colunas do datafrane criado com merge (df)
df.columns = ['zipcode', 'houses', 'price mean', 'living  mean', 'price/m^2']

#st.dataframe(df)
c1.header('Metrics')
c1.dataframe(df)

#==========================#===================#==================#================
# # Métricas - Segunda  opção (melhor)
# df1 = data[['id']].count().reset_index()

# ## Média de preço por região
# df2 = data[['price']].mean().reset_index()

# ## média da sala de estar por região
# df3 = data[['sqft_living']].mean().reset_index()

# ## média de preços por metro quadrado, por região
# df4 = data[['price_m^2']].mean().reset_index()

# df = pd.concat([df1, df2, df3, df4], axis=0)
# st.write(df)
#==========================#===================#==================#================

#################        Estatísticas descritivas          ######################

num_attributes = data.select_dtypes(include=['int64', 'float64']) # dataframe que contém apenas os elementos numéricos (apenas as colunas que têm números)
media = pd.DataFrame(num_attributes.apply(np.mean))
mediana = pd.DataFrame(num_attributes.apply(np.median))
desvio = pd.DataFrame(num_attributes.apply(np.std))
max_ = pd.DataFrame(num_attributes.apply(np.max))
min_ = pd.DataFrame(num_attributes.apply(np.min))

df_stats = pd.concat([media, max_, min_, desvio, mediana], axis=1).reset_index()

df_stats.columns = ['attributes', 'media', 'max_', 'min_', 'desvio', 'mediana']

#st.dataframe(df_stats)
c2.header('Stats')
c2.dataframe(df_stats)


#=======================================================================
#                Densidade de portfolio - Mapas 
#=======================================================================
st.title('Region Overview')

#### Mapa 1 - agrupamento de marcadores por "lat" e "long"
df1 = data.sample(10) # seleciona apenas mil itens de 'data'

#  Mapa Base  - (biblioteca Folium)
density_map = folium.Map(location = [data['lat'].mean(), # plota um mapa base com os dados de 'lat' e 'long' de 'data' (padrão)
                                     data['long'].mean()], 
                                     default_zoom_start = 8,
                                     width=600,
                                     height=600,
                                     control_scale=True)

cluster_ = MarkerCluster().add_to(density_map) # Agrupa os pontos no mapa, (marcadores)
for name, row in df1.iterrows(): # coloca os marcadores no mapa (pontos que representam as casas)
    folium.Marker([row['lat'], row['long']],
        popup= # serve para inserir uma caixa de diálogo com informações (no caso, preço, tamanho da sala, n° de banheiros...)
        'Sold R${0} on: {1}. Features: {2} squarefeet, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                                                                                                            row['price'], 
                                                                                                            row['date'], 
                                                                                                            row['sqft_living'], 
                                                                                                            row['bedrooms'], 
                                                                                                            row['bathrooms'], 
                                                                                                            row['yr_built'])).add_to(cluster_)

#c1.header('Portfolio Density')

#with c1:
#    folium_static(density_map) # Plota o mapa, no lado esquerdo, c1


### Mapa 2 - Média de preços por região

df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df2.columns = ['ZIP', 'PRICE']

#df2 = df2.sample(10)

geofile = geofile[geofile['ZIP'].isin(df2['ZIP'].tolist())] # filtro para mostrar apenas as zonas que contém os zipcodes que estão no dataset , caso contrário, geofile mostra todas as zonas.

region_price_map = folium.Map(location = [data['lat'].mean(),
                                          data['long'].mean()],
                                          default_zoom_start = 8,
                                          width=600, 
                                          height=600, 
                                          control_scale=True)

folium.Choropleth(data = df2,
                  geo_data = geofile,
                  columns= ['ZIP', 'PRICE'],
                  key_on = 'feature.properties.ZIP',
                  fill_color ='YlOrRd',
                  fill_opacity = 0.7,
                  line_opacity = 0.2,
                  legend_name = 'Avg Price').add_to(region_price_map)



c1, c2 = st.columns((1, 1))
c1.header('Portfolio Density')
c2.header('Price Density')

with c1:
    folium_static(density_map) # Plota o mapa, no lado esquerdo, c1

with c2:
    folium_static(region_price_map)

#==============================================================================
#               Distribuição dos imóveis por categorias comerciais
#==============================================================================
st.sidebar.title('Commercial Options')
st.title('Commercial Attributes')

## -----Preço médio por ano

# Filtros 
min_yr_built = int(data['yr_built'].min()) #seleciona o mínimo e transforma em número inteiro (int64)
max_yr_built = int(data['yr_built'].max()) #seleciona o máximo e transforma em número inteiro (int64)

st.sidebar.subheader('Select max year built')
f_yr_built = st.sidebar.slider('Year Built:', min_yr_built, max_yr_built, max_yr_built) # botão de filtro, do tipo slider, onde os parâmetros são: (texto, valor min, valor max, default)

st.header('Average Price per Year Built')

# Seleção dos dados
df = data[data['yr_built'] < f_yr_built] # Seleciona apenas os valores menores que os indicados no botão do filtro e guarda em df.
df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

# Plotagem
fig = px.line(df, x='yr_built', y='price')
st.plotly_chart(fig, use_container_width=True)

## -----Preço médio por dia
st.header('Average Price per Day')
st.sidebar.subheader('Select max date')

data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')

# Filtros
min_date = datetime.strptime(data['date'].min(), '%Y-%m-%d') #seleciona o mínimo e transforma em data (datetime64[ns])
max_date = datetime.strptime(data['date'].max(), '%Y-%m-%d') #seleciona o máximo e transforma em data (datetime64[ns])

f_date = st.sidebar.slider('Date:', min_date, max_date, max_date) # botão de filtro, do tipo slider.

# Seleção dos dados
data['date'] = pd.to_datetime(data['date'])
df = data[data['date'] < f_date]
df = df[['date', 'price']].groupby('date').mean().reset_index()

# Plotagem
fig = px.line(df, x='date', y='price')
st.plotly_chart(fig, use_container_width=True)


# -----------Histograma
st.header('Price Distribution')
st.sidebar.subheader('Select max price')

# Filtros
min_price = int(data['price'].min())
max_price = int(data['price'].max())
avg_price = int(data['price'].mean())

# Seleção dos dados
f_price = st.sidebar.slider('Price:', min_price, max_price, avg_price)
df = data[data['price'] < f_price]

# Plotagem
fig = px.histogram(df, x='price', nbins=50)
st.plotly_chart(fig, use_container_width=True)

#==============================================================================
#               Distribuição dos imóveis por categorias físicas
#==============================================================================
st.sidebar.title('Attributes Options')
st.title('House Attributes')

######## Houses per bedrooms ########
#Filtros
f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', sorted(set(data['bedrooms'].unique())))
#Seleção dos dados
df_bed = data[data['bedrooms'] < f_bedrooms]
#figura
fig_bed = px.histogram(df_bed, x='bedrooms', nbins=19)
st.plotly_chart(fig_bed, use_container_width=True)


######## Houses per bathrooms ########
#Filtros
f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', sorted(set(data['bathrooms'].unique())))
#Seleção dos dados
df_bth = data[data['bathrooms'] < f_bathrooms]
#figura
fig_bth = px.histogram(df_bth, x='bathrooms', nbins=19)
st.plotly_chart(fig_bth, use_container_width=True)


######## Houses per floors ########
#Filtros
f_floors = st.sidebar.selectbox('Max number of floors', sorted(set(data['floors'].unique())))
#Seleção dos dados
df_flr = data[data['floors'] < f_floors]
#figura
fig_flr = px.histogram(df_flr, x='floors', nbins=19)
st.plotly_chart(fig_flr, use_container_width=True)


######## Houses per waterview ########
f_waterview = st.sidebar.checkbox('Only Houses with Waterview')

if f_waterview:
    df_wtv = data[data['waterfront'] == 1]
else:
    df_wtv = data.copy()

fig_wtv = px.histogram(df_wtv, x='waterfront', nbins=10)
st.plotly_chart(fig_wtv, use_container_width=True)
