import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static


# Streamlit -> Framework para desenvolvimento de dashboards interativos
# Folium -> Biblioteca de convecção de mapa
# Plotly -> Biblioteca de plotagem de gráficos
# pandas e geopandas -> Bibliotecas para processamento de dados
# Streamlit-static ->Biblioteca de integração do streamlit com o folium

class PaginaWeb:

    def ler_arquivo(arquivo):
        gdf = gpd.read_file(arquivo)
        return gdf
        
    def resumo(gdf):
        # divisão em colunas para melhor visualização
        col1, col2 = st.columns(2)
        with col1:
                                # retirando a coluna geometry que é desnecessária
            col1 = st.dataframe(gdf.drop(columns=['geometry']), height=317)
        with col2:
            col2 = st.dataframe(gdf.describe(),height=317)
    
    def grafico(df):      
        df = pd.DataFrame(df)
        # criando gráficos com seletores para os eixos x e y
        col1_tipo_grafico, col2, col3 = st.columns(3)
        # selecionando o tipo de  gráfico
        tipo_grafico = col1_tipo_grafico.selectbox('Selecione o tipo do gráfico',options=['box', 'bar', 'line', 'scatter', 'violin', 'histogram'], index=5)
        # selecioando os valores para os eixos x e y do gráfico                             index seleciona um valor padrao
        x_val = col2.selectbox('Selecione o eixo x do gráfico',options=df.columns, index=1)
        y_val = col3.selectbox('Selecione o eixo y do gráfico',options=df.columns, index=3)

        # faz a junção da função px com a variavel tipo_grafico
        plot_func = getattr(px, tipo_grafico)

        plot = plot_func(df, x_val, y_val)
        # use_container_width é para o grafico realizar o ajuste de tamanho
        st.plotly_chart(plot, use_container_width=True)
 
    def mapa(gdf):
        mapa = folium.Map(location=[-20.5, -54.5], zoom_start=7, control_scale=True, tiles='Esri World Imagery')
        #passo o geo_dataframe e adiciona o mapa o folium Geojson
        folium.GeoJson(gdf).add_to(mapa)
    
        # recupera os limites da geometria (por arquivo)
        bounds = gdf.total_bounds
        #st.write(bounds) visualizar os valores dos limites

        # configura o tamanho da area conforme as limites da geometria
        # passando os valores maximos e minimos de x e y
        # O formato correto é [min_lat, min_lon, max_lat, max_lon]
        mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
        # adicionando controle de camadas ao mapa
        folium.LayerControl().add_to(mapa)

        # desenhar o mapa
        folium_static(mapa, width=650, height=400)

if __name__ == '__main__':
    st.sidebar.header('Menu')
    arquivo = st.sidebar.file_uploader('Selecione o arquivo')
    if arquivo:
        # Colocando um cabeçalho
        st.header('Dashboar Interativo')
        # Criando uma instância da classe
        pwb = PaginaWeb
        # lendo um arquivo
        gdf = pwb.ler_arquivo(arquivo)        
        # criando um radio para seleção das opções
        elemento = st.sidebar.radio ('Selecione o elemento a ser visualizado.', options=['Mapa', 'Grafico', 'Tabela'])
        if elemento == 'Mapa':
            pwb.mapa(gdf)
        elif elemento == 'Grafico':
            pwb.grafico(gdf)
        elif elemento == 'Tabela':
            pwb.resumo(gdf)
    else:
        st.warning('Selecione um arquivo.')
    
    
    
