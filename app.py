import streamlit as st
from pipeline.main_pipe import main_pipeline

#========================================================
#CONFIGS
page_title = "Recomendador de Time Pokemon"
layout = "wide"
st.set_page_config(page_title=page_title, layout=layout)

#========================================================
#CONEXÃO
#Paths dos arquivos de entrada
path_pokemons ='data/pokemon_1.csv'
path_gymLeaders = 'data/PokemonGymLeaders.csv'
path_typeChart ='data/chart_type.csv' 
path_imagens = 'data\images'

st.title("POKEMON RECOMENDADOR")

main_pipeline(path_pokemons, path_gymLeaders, path_typeChart, path_imagens)