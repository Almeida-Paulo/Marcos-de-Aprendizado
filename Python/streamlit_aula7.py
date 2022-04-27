import pandas as pd
import streamlit as st
import numpy as np
import folium
import geopandas

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

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


f_attributes = st.sidebar.multiselect('Enter columns', data.columns) # filtro para as colunas

f_zipcode = st.sidebar.multiselect(
    'Enter zipcode', 
    data['zipcode'].unique()) # filtra as linhas pelo número do zipcode. unique() verifica todos os valores de zipcode que existem nas linhas

st.title('Data Overview')

if (f_zipcode != []) & (f_attributes != []): # significa que um filtro por zipcode e um filtro por coluna estão selecionados. ## "!= []" (diferente de vazio), está selecionado;
    data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes] 

elif (f_zipcode != []) & (f_attributes == []): # ## "== []" (igual a vazio), não está selecionado.
    data = data.loc[data['zipcode'].isin(f_zipcode), :] # o termo ":" significa que todas as colunas serão mostradas (selecionadas)

elif (f_zipcode == []) & (f_attributes != []): 
    data = data.loc[:, f_attributes] # # o termo ":" significa que todas as linhas serão mostradas.

else:
    data = data.copy()


st.dataframe(data)

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


num_attributes = data.select_dtypes(include=['int64', 'float64']) # dataframe que contém apenas os elementos numéricos (apenas as colunas que têm números)
media = pd.DataFrame(num_attributes.apply(np.mean))
mediana = pd.DataFrame(num_attributes.apply(np.median))
desvio = pd.DataFrame(num_attributes.apply(np.std))
max_ = pd.DataFrame(num_attributes.apply(np.max))
min_ = pd.DataFrame(num_attributes.apply(np.min))

df_stats = pd.concat([media, max_, min_, desvio, mediana], axis=1).reset_index()

df_stats.columns = ['attributes', 'media', 'max_', 'min_', 'desvio', 'mediana']

c2.header('Stats')
c2.dataframe(df_stats)


st.title('Region Overview')
c1, c2 = st.columns((1, 1))
c1.header('Portfolio Density')

#### Mapa 1 - agrupamento de marcadores por "lat" e "long"
df1 = data.sample(10) 

density_map = folium.Map(location = [data['lat'].mean(), # plota um mapa base com os dados de 'lat' e 'long' de 'data' (padrão)
                                     data['long'].mean()], 
                                     default_zoom_start = 8)

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

with c1:
    folium_static(density_map) # Plota o mapa, no lado esquerdo, c1


c2.header('Price Density')

df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df2.columns = ['ZIP', 'PRICE']

#df2 = df2.sample(10)

geofile = geofile[geofile['ZIP'].isin(df2['ZIP'].tolist())]

region_price_map = folium.Map(location = [data['lat'].mean(),
                                          data['long'].mean()],
                                          default_zoom_start = 8)

folium.Choropleth(data = df2,
                        geo_data = geofile,
                        columns= ['ZIP', 'PRICE'],
                        key_on = 'feature.properties.ZIP',
                        fill_color ='YlOrRd',
                        fill_opacity = 0.7,
                        line_opacity = 0.2,
                        legend_name = 'Avg Price').add_to(region_price_map)

with c2:
    folium_static(region_price_map)