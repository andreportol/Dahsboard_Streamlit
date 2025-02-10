import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static


# adicionando titulo
st.title('Aula Pro Ambiental')
# adicionando sub cabeçalho
st.subheader('Dados de Mato Grosso do Sul')
# adicionando um sitebar
st.sidebar.subheader('Menu')
# adicionando um botão para upload do arquivo
arquivo_upload = st.sidebar.file_uploader('Selecione o arquivo!')

if arquivo_upload:
    # ler o arquivo atráves do geopandas
    gdf = gpd.read_file(arquivo_upload)
    #organizando os elementos 
    col1, col2 = st.columns(2)

    with col1:
        # escreve na tela, porém não tem controle de altura
        #st.write(gdf)
        st.dataframe(gdf, height=320)
    with col2:
        # describe -> Realiza calculos automaticos
        st.dataframe(gdf.describe(), height=320)
        #st.write(gdf.describe())

    #Criando um df em pandas, para isso é 
    #passado o geodataframe criado e retirando a coluna
    #geometry, nesse caso é interessante fazer isso pois iremos gerar
    #gráficos e não há necessidade de uma coluna de geometry. Lembrando
    #que essa coluna é pesada e que pode demorar o processamento.

    df = pd.DataFrame(gdf).drop(columns=['geometry'])
    st.write(df)


    # criando gráficos com seletores para os eixos x e y
    col1_tipo_grafico, col2_grafico, col3_grafico = st.columns(3)
    # selecionando o tipo de  gráfico
    tipo_grafico = col1_tipo_grafico.selectbox('Selecione o tipo do gráfico',options=['box', 'bar', 'line', 'scatter', 'violin', 'histogram'], index=5)
    # selecioando os valores para os eixos x e y do gráfico                             index seleciona um valor padrao
    x_val = col2_grafico.selectbox('Selecione o eixo x do gráfico',options=df.columns, index=1)
    y_val = col3_grafico.selectbox('Selecione o eixo y do gráfico',options=df.columns, index=3)
    

    # faz a junção da função px com a variavel tipo_grafico
    plot_func = getattr(px, tipo_grafico)

    plot = plot_func(df,x=x_val,y=y_val)
    # use_container_width é para o grafico realizar o ajuste de tamanho
    st.plotly_chart(plot, use_container_width=True)

    mapa = folium.Map(location=[-20.5, -54.5], zoom_start=7, control_scale=True, tiles='Esri World Imagery')

    # retirando colunas desnecessárias
    #gdf = gdf.drop(columns=['data'])

    #passo o geo_dataframe e adiciona o mapa o folium Geojson
    folium.GeoJson(gdf).add_to(mapa)

    # configuração do zoom do mapa
    # recupera os limites da geometria (por arquivo)
    bounds = gdf.total_bounds
    #st.write(bounds)

    # configura o tamanho da area conforme as limites da geometria
    # passando os valores maximos e minimos de x e y
    # O formato correto é [min_lat, min_lon, max_lat, max_lon]
    mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
    # adicionando controle de camadas ao mapa
    folium.LayerControl().add_to(mapa)

    # desenhar o mapa
    folium_static(mapa, width=500, height=500)
else:
    st.warning('Selecione o arquivo.')