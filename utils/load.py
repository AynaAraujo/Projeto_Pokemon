import sqlite3

def df_to_pandas(df):
  #Convertendo os dfs do pyspark para Pandas's df
  df_pd = df.toPandas()
  return df_pd

def load_no_banco(df,tableName):
  #Criando conexão com o banco de dados
  conn = sqlite3.connect("pokemon.db")
  cursor = conn.cursor()

  #Incluindo os Dfs no banco
  df.to_sql(tableName, conn, if_exists="replace", index=False)

  #Fecha Conexão
  conn.close()