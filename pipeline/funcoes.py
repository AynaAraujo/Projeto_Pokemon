import streamlit as st
from utils.extract import *

from utils.Filter.filtrando_gymLeaders import filtered_gym_leaders
from utils.Filter.filtrando_pokemon import *
from utils.Filter.filtrando_typeCharts import ajuste_TypeChart

from utils.load import *

from utils.load_img import show_photo

from recomendador.analisa_gymLeaders import *

from recomendador.analisa_fraquezas import *

from recomendador.montando_time import * 



def selecionando_jogo():
    #Selecionando o JOGO
    game_name = st.selectbox("Qual o nome do jogo?",
                             ['Red','Gold','Silver','Crystal','Ruby','Sapphire','Emerald',
                              'Fire Red','Leaf Green','Diamond','Pearl','Platinum','Heart Gold','Soul Silver',
                              'Black','White','Black 2','White 2','X','Y','Sun','Moon','Ultra Sun','Ultra Moon',
                              'Sword','Shield','Scarlet','Violet'])
    if game_name:
      idGame = choose_game(game_name)
      poke_numbers = pegando_pokedex(idGame)
    return game_name,idGame,poke_numbers


def criar_dfs(path_pokemons, path_gymLeaders, path_typeChart):
    #Criando Dfs
    dados_pokemon = criar_df(path_pokemons)
    dados_gymLeaders = criar_df(path_gymLeaders,sep = ";")
    dados_typeChart = criar_df(path_typeChart)
    return dados_pokemon,dados_gymLeaders,dados_typeChart


def tratando_dfs(dados_pokemon,poke_numbers,dados_gymLeaders,dados_typeChart):
    #Tratando Dfs
    ##DF POKEMON
    dados_pokemon_new = tratando_pokemon_df(dados_pokemon)
    dados_pokemon_filtered = limpando_pokemon_df(dados_pokemon_new)
    dados_pokemon_final = select_pokemons(dados_pokemon_filtered,poke_numbers)
    ##DF GYM LEADERS
    dados_gymLeaders_final = filtered_gym_leaders(dados_gymLeaders)
    ##DF TypeCharts
    dados_typeChart_final = ajuste_TypeChart(dados_typeChart)
    return dados_pokemon_final,dados_gymLeaders_final,dados_typeChart_final


# Em pipeline/funcoes.py, dentro de criar_banco
def criar_banco(dados_pokemon_final,dados_gymLeaders_final,dados_typeChart_final):

    #Criando Banco
    ##Convertendo Dfs
    # *** ESTAS LINHAS DE DEBUG SÃO CRUCIAIS ***
    # print("\n--- DEBUG: Esquema de dados_typeChart_final antes de df_to_pandas ---")
    # dados_typeChart_final.printSchema() # Esta linha imprime o esquema
    # print("\n--- DEBUG: Primeiras 5 linhas de dados_typeChart_final ---")
    # dados_typeChart_final.show(5, truncate=False) # Esta linha imprime os dados
    # print("-------------------------------------------------------------------\n")
    # *******************************************

    df_dados_typeChart_final  = df_to_pandas(dados_typeChart_final)
    df_dados_gymLeaders_final = df_to_pandas(dados_gymLeaders_final)
    df_dados_pokemon_final =  df_to_pandas(dados_pokemon_final)
    ##Subindo no Banco
    load_no_banco(df_dados_typeChart_final,"Type_Charts")
    load_no_banco(df_dados_gymLeaders_final,"Gym_Leaders")
    load_no_banco(df_dados_pokemon_final,"Pokemons")
    return df_dados_typeChart_final,df_dados_gymLeaders_final,df_dados_pokemon_final

def analise_poke_rivais(game_name):
  ##Analisando Pokemons dos Gym Leaders
  list_poke_rivals = get_rival_pokemons(game_name)
  types_1, types_2 = count_rival_types(list_poke_rivals)
  print('+'*30)
  most_common_types = get_most_common_types(types_1, types_2 )
  return most_common_types


def analise_fraquezas(most_common_types,df_dados_typeChart_final):
  ##Analisando Fraquezas
  df_dados_typeChart_final = set_first_column_as_index(df_dados_typeChart_final)
  tipos_ideias = get_top_effective_types(most_common_types,df_dados_typeChart_final)
  return tipos_ideias


def escolhendo_inicial(poke_numbers,df_dados_pokemon_final,path_imagens):
  poke_starters = poke_numbers[:9]
  ###Escolhendo Inicial
  starter_name = choose_initial_pokemon(df_dados_pokemon_final, poke_numbers, path_imagens)
  st.write("Você escolheu:", starter_name)
  poke_starter = get_initial_pokemon_info(starter_name)
  poke_starter_final_form = get_final_form_info(poke_starter[1])
  return poke_starter_final_form, poke_starters


def montando_time(tipos_ideias,poke_starters,poke_starter_final_form,dados_pokemon_final,path_imagens):
  ###Estruturando o Time
  poke_chosen =  build_pokemon_team(tipos_ideias, poke_starters, poke_starter_final_form)
  poke_team = get_names(poke_chosen)
  meu_time =  show_time(dados_pokemon_final,poke_team,path_imagens)
  return poke_chosen


def outras_opcoes(poke_chosen,poke_starters,dados_pokemon_final,path_imagens):
  #EXTRA - outras opções de pokemons
  st.write('=='*30)
  infos = get_other_options(poke_chosen,poke_starters)
  info_names = get_names(infos)
  st.subheader('Outras Opções de Pokémon')
  other_team = show_time(dados_pokemon_final,info_names,path_imagens,text = "OUTROS POKEMONS")
  


