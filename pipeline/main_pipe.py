from .funcoes import selecionando_jogo
from .funcoes import criar_dfs
from .funcoes import tratando_dfs
from .funcoes import criar_banco
from .funcoes import analise_poke_rivais
from .funcoes import analise_fraquezas
from .funcoes import escolhendo_inicial
from .funcoes import montando_time
from .funcoes import outras_opcoes

path_imagens = 'data\images'

def main_pipeline(path_pokemons, path_gymLeaders, path_typeChart, path_imagens):
  #Selecionando Jogo
  game_name,idGame,poke_numbers = selecionando_jogo()
  #criar_dfs
  dados_pokemon, dados_gymLeaders, dados_typeChart = criar_dfs(path_pokemons, path_gymLeaders, path_typeChart)
  #Tratando Dfs
  dados_pokemon_final,dados_gymLeaders_final,dados_typeChart_final =  tratando_dfs(dados_pokemon,poke_numbers,dados_gymLeaders,dados_typeChart)
  #Criando Banco
  df_dados_typeChart_final,df_dados_gymLeaders_final,df_dados_pokemon_final = criar_banco(dados_pokemon_final,dados_gymLeaders_final,dados_typeChart_final)
  ##Analisando Pokemons dos Gym Leaders
  most_common_types = analise_poke_rivais(game_name)
  ##Analisando Fraquezas
  tipos_ideias = analise_fraquezas(most_common_types,df_dados_typeChart_final)
  ###Escolhendo Inicial
  poke_starter, poke_starters = escolhendo_inicial(poke_numbers,df_dados_pokemon_final,path_imagens)
  ###Estruturando o Time
  meu_time = montando_time(tipos_ideias,poke_starters,poke_starter,dados_pokemon_final,path_imagens)
  #EXTRA - outras opções de pokemons
  other_team = outras_opcoes(meu_time,poke_starters,dados_pokemon_final,path_imagens)

