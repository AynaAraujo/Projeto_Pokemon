import sqlite3

#Pega os pokenons dos rivais
def get_rival_pokemons(game_name, db_path = "pokemon.db"):
    """
    Retorna os Pokémons dos líderes de ginásio (rivais) para um jogo específico.

    Parâmetros:
    - game_name: Nome (ou parte) do jogo para busca.
    - db_path: Caminho para o banco de dados SQLite.

    Retorna:
    - Lista de strings com os Pokémons de cada líder.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT GROUP_CONCAT("Pokemon", ', ')
    FROM Gym_Leaders
    WHERE Game LIKE ?
    GROUP BY "Gym leader"
    '''

    cursor.execute(query, (f"%{game_name}%",))
    rows = cursor.fetchall()

    conn.close()

    # Apenas para debug/visualização durante a execução da pipeline
    print("--" * 30)
    for row in rows:
        print(row)

    # Convertendo a tupla numa lista
    list_poke_rivals = [poke.strip() for sublist in rows for poke in str(sublist[0]).split(", ") if poke]

    return list_poke_rivals


#Faz a contagem dos tipos de cada pokémon
def count_rival_types(pokemon_names, db_path ="pokemon.db"):
    """
    Conta os tipos primário e secundário dos Pokémons rivais.

    Parâmetros:
    - pokemon_names: Lista de nomes dos Pokémons.
    - db_path: Caminho para o banco de dados SQLite.

    Retorna:
    - Uma tupla contendo:
        - Lista de tuplas com (Tipo 1, contagem)
        - Lista de tuplas com (Tipo 2, contagem)
    """
    if not pokemon_names:
        return [], []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders = ", ".join("?" * len(pokemon_names))

    query_1 = f'''
    SELECT "Type 1", COUNT("Type 1") AS Main
    FROM Pokemons
    WHERE Name IN ({placeholders})
    GROUP BY "Type 1"
    ORDER BY Main DESC
    '''

    cursor.execute(query_1, pokemon_names)
    types_rivais_1 = cursor.fetchall()

    print("--" * 30)
    print("Tipo Primário:")
    for row in types_rivais_1:
        print(row)

    query_2 = f'''
    SELECT "Type 2", COUNT("Type 2") AS Main
    FROM Pokemons
    WHERE Name IN ({placeholders})
    GROUP BY "Type 2"
    ORDER BY Main DESC
    '''

    cursor.execute(query_2, pokemon_names)
    types_rivais_2 = cursor.fetchall()

    print("--" * 30)
    print("Tipo Secundário:")
    for row in types_rivais_2:
        print(row)

    conn.close()
    return types_rivais_1, types_rivais_2


#Rankeia os tipos por ocorrência e retorna os 6 mais comuns
def get_most_common_types(types_1, types_2, top_n= 6) -> list:
    """
    Combina os tipos primários e secundários dos Pokémons rivais,
    eliminando repetições e retornando os `top_n` mais comuns.

    Parâmetros:
    - types_1: Lista de tuplas com (tipo primário, contagem)
    - types_2: Lista de tuplas com (tipo secundário, contagem)
    - top_n: Quantidade de tipos mais comuns a retornar (default = 6)

    Retorna:
    - Lista com os nomes dos tipos mais comuns
    """
    lista = []

    for n in range(len(types_1)):
        for m in range(len(types_2)):
            if types_1[n][1] <= types_2[m][1]:
                if types_2[m][0] and not any(item[0] == types_2[m][0] for item in lista):
                    lista.append([types_2[m][0], types_2[m][1]])

        if types_1[n][0] and not any(item[0] == types_1[n][0] for item in lista):
            lista.append([types_1[n][0], types_1[n][1]])

    most_types = lista[:top_n]
    most_common_types = [tipo[0] for tipo in most_types]

    return most_common_types



