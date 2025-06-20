from pyspark.sql.functions import col, when


def filtered_gym_leaders(df):
  dados_gymLeaders = df

  #Filtrando colunas úteis
  dados_gymLeaders_filtered = dados_gymLeaders\
                              .select(['Game','Gym leader','Pokemon'])

  #Adicionando Novas Versões
  dados_gymLeaders_final = dados_gymLeaders_filtered.withColumn(
                                    "Game",
                                    when(col("Game") == "Red", "Red/Fire Red")
                                    .when(col("Game") == "Blue", "Blue/Leaf Green")
                                    .when(col("Game") == "Yellow", "Yellow/Special Pikachu Edition")
                                    .when(col("Game") == "Gold", "Gold/HeartGold")
                                    .when(col("Game") == "Silver", "Silver/SoulSilver")
                                    .when(col("Game") == "Ruby", "Gold/Omega Ruby")
                                    .when(col("Game") == "Sapphire", "Silver/Alpha Sapphire")
                                    .when(col("Game") == "Brilliant Diamond", "Brilliant Diamond/Shining Pearl")
                                    .when(col("Game") == "Shining Pearl", "Brilliant Diamond/Shining Pearl")
                                    .otherwise(col("Game"))
)

  return dados_gymLeaders_final


