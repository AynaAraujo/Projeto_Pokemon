from pyspark.sql import functions as F
from pyspark.sql.functions import col, when


def tratando_pokemon_df(df):
  dados_pokemon = df

  #trocar o nome da coluna '#' por entry_number
  dados_pokemon_new = dados_pokemon\
                      .withColumnRenamed('Index','entry_number')

  #criar uma coluna para os pokemons Míticos e Lendários,pois não aparecem livremente na natureza.
  legendary_pokemon = [144,145,146,150,243,244,245,249,250,377,378,379,380,381,382,383,384,480,481,482,483,484,
                     485,486,487,488,638,639,640,641,642,643,644,645,646,716,717,718,772,773,785,786,787,788,
                     789,790,791,792,793,794,795,796,797,798,799,800,803,804,805,806,888,889,890,891,892,894,
                     895,896,897,898,905,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,
                     1016,1017]

  mythical_pokemon=[151,251,385,386,489,490,491,492,493,494,647,648,649,719,720,721,801,802,807,808,809,893,1001]
  dados_pokemon_new = dados_pokemon_new\
                      .withColumn("Legendary",col("entry_number").isin(legendary_pokemon))\
                      .withColumn("Mythical",col("entry_number").isin(mythical_pokemon))


  #criar um novo dataframe apenas com as colunas que irei utilizar e Ajustando Type 2
  dados_pokemon_new_filtered = dados_pokemon_new\
                                  .select(['entry_number','Name','Type 1','Type 2','Total','Legendary','Mythical','Image'])\
                                  .withColumn("Type 2", when(col("Type 2").isNull(), col("Type 1")).otherwise(col("Type 2")))

  return dados_pokemon_new_filtered


def limpando_pokemon_df(df):
  dados_pokemon_new_filtered = df

  #Novo dataframe contendo  a coluna 'count' que diz quantas vezes ele aparece
  count_df = dados_pokemon_new_filtered\
      .groupBy('entry_number')\
      .agg(F.count('entry_number').alias('count'))

  dados_pokemon_com_count = dados_pokemon_new_filtered\
                              .join(count_df, on="entry_number", how="left")

  #Criando novo dataframe sem as linhas com Versões Alternativas
  #Df com os pokemons alternativos
  alt_pokemon = dados_pokemon_com_count\
                    .select('*')\
                    .filter((dados_pokemon_com_count['count'] > 1) &((dados_pokemon_com_count['Name'].like('%Mega%') )
                    | (dados_pokemon_com_count['Name'].like('%Hisuian%'))
                    | (dados_pokemon_com_count['Name'].like('%Breed%'))
                    | (dados_pokemon_com_count['Name'].like('%Partner%'))
                    )
                    )

  # Realizando o anti join para remover as linhas de dados_pokemon_new_filtered que estão em mega_pokemon
  dados_pokemon_final = dados_pokemon_new_filtered\
      .join(alt_pokemon, 'Name', 'left_anti')

  #Filtrando formas que só aparecem em jogos específicos

  count_df = dados_pokemon_final\
    .groupBy('entry_number')\
    .agg(F.count('entry_number').alias('count'))

  # Join the count back to the original DataFrame
  dados_pokemon_com_count = dados_pokemon_final\
      .join(count_df, on="entry_number", how="left")

  alolan_poke = dados_pokemon_com_count\
      .filter((F.col('count') > 1) & (F.col('Name').like('%Alolan%')))

  galar_poke = dados_pokemon_com_count\
      .filter((F.col('count') > 1) & (F.col('Name').like('%Galarian%')))

  paldea_poke = dados_pokemon_com_count\
      .filter((F.col('count') > 1) & (F.col('Name').like('%Paldean%')))


  # Verificando se é necessário remover
  if id != 8:
      dados_pokemon_final = dados_pokemon_final\
          .join(alolan_poke.select('Name'), on='Name', how='left_anti')
  if id !=9:
      dados_pokemon_final = dados_pokemon_final\
          .join(galar_poke.select('Name'), on='Name', how='left_anti')
  if id !=10:
      dados_pokemon_final = dados_pokemon_final\
          .join(paldea_poke.select('Name'), on='Name', how='left_anti')

  return dados_pokemon_final


def select_pokemons(df,poke_numbers):
  dados_pokemon_final = df
  dados_pokemon_new = dados_pokemon_final\
                      .select('*')\
                      .filter(dados_pokemon_final['entry_number'].isin(poke_numbers))
  print(f"Qtd de Pokemons:{dados_pokemon_new.count()}")
  return dados_pokemon_new



