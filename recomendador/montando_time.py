import sqlite3
import streamlit as st
from utils.load_img import show_photo

def choose_initial_pokemon(df, poke_numbers, path_imagens):
    """
    Mostra ao usuário três Pokémons iniciais e permite escolher um deles.
    """
    poke_starters = poke_numbers[:9]
    poke_options = [poke_starters[0], poke_starters[3], poke_starters[6]]

    st.subheader("Escolha seu Pokémon inicial:")

    # Filtra o DataFrame para os Pokémons escolhidos
    starter_df = df[df['entry_number'].isin(poke_options)]

    nomes_validos = []

    for _, row in starter_df.iterrows():
        nome = row['Name']
        imagem = row['Image']
        nomes_validos.append(nome.lower())  # Guardamos versão minúscula

        st.write(f"Pokémon: {nome}")
        show_photo([imagem], path_imagens)
        st.write("-" * 20)

    while True:
        starter_name = st.selectbox("Digite o nome do Pokémon escolhido:", nomes_validos)
        if starter_name:
            if starter_name.lower() in nomes_validos:
                # Padroniza o nome como está no banco
                for nome in nomes_validos:
                    if starter_name.lower() == nome:
                        index = nomes_validos.index(nome)
                        starter_name = list(starter_df['Name'])[index]
                        break
                break
            else:
                print("Nome inválido. Digite exatamente o nome de um dos Pokémons exibidos.")

    return starter_name


def get_initial_pokemon_info(starter_name):
    """
    Busca informações do Pokémon inicial pelo nome (case-insensitive)
    Retorna: Lista com os dados do Pokémon ou None se não encontrar
    """
    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM Pokemons WHERE LOWER(Name) = LOWER(?)', (starter_name,))
        pokemon_data = cursor.fetchone()

        if pokemon_data:
            print(f"\nPokémon inicial encontrado: {pokemon_data[2]} (Nº{pokemon_data[1]})")
            return pokemon_data
        else:
            print(f"\nPokémon '{starter_name}' não encontrado!")
            return None

    finally:
        conn.close()


def get_final_form_info(entry_number):
    """
    Busca a evolução final (entry_number + 2)
    Retorna:
        - Tupla com todos os dados do Pokémon evoluído se encontrar
        - None se não encontrar
    """
    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()
    rows = None  # Inicializa rows como None

    try:
        final_entry = entry_number + 2
        cursor.execute('SELECT * FROM Pokemons WHERE entry_number = ?', (final_entry,))
        rows = cursor.fetchall()  # Mantém o fetchall como no seu original

        if rows:
            print(f"Evolução final encontrada: {rows[0][2]} (Nº{rows[0][1]})")  # Assumindo que nome está no índice 2
        else:
            print(f"Evolução final não encontrada para Nº{entry_number} (busca por Nº{final_entry})")

    finally:
        conn.close()

    return rows  # Retorna a lista de tuplas como no seu código original


def build_pokemon_team(tipos_ideais, poke_starters, inicial_poke, db_path="pokemon.db", team_size=6):
    """
    Constrói um time de Pokémon recomendados com base nos tipos ideais, garantindo diversidade de tipos.
    Opcionalmente adiciona um Pokémon inicial, substituindo Pokémon existentes quando necessário.

    Parâmetros:
    - tipos_ideais: lista de tipos desejados (ex: ['Fire', 'Grass'])
    - poke_starters: lista de entry_numbers dos pokémons iniciais (ex: [1, 4, 7])
    - inicial_poke: Pokémon inicial a ser considerado para inclusão no time (opcional)
    - db_path: caminho para o arquivo do banco de dados
    - team_size: tamanho máximo do time (padrão: 6)

    Retorna:
    - Lista de tuplas com os Pokémon selecionados para o time
    """
    # Passo 1: Obter os Pokémon recomendados do banco de dados
    poke_recomendados = get_recommended_pokemons(tipos_ideais, poke_starters, db_path)

    # Passo 2: Selecionar os Pokémon para o time garantindo diversidade de tipos
    poke_chosen = []
    poke_chosen_types = []

    for pokemon in poke_recomendados:
        if len(poke_chosen) >= team_size:
            break

        type1 = pokemon[2]  # Assumindo que Type 1 está no índice 2
        type2 = pokemon[3] if len(pokemon) > 3 else None  # Type 2 pode ser None

        if type1 in tipos_ideais and type1 not in poke_chosen_types:
            poke_chosen.append(pokemon)
            poke_chosen_types.append(type1)
        elif type2 and type2 in tipos_ideais and type2 not in poke_chosen_types:
            poke_chosen.append(pokemon)
            poke_chosen_types.append(type2)

    # Passo 3: Processar o Pokémon inicial, se fornecido
    if inicial_poke and len(inicial_poke) > 0:
        weakest = [1000, -1]  # [lowest_stat, index]

        if len(poke_chosen) < team_size:
            poke_chosen.append(inicial_poke[0])  # Adiciona se o time não está completo
        else:
            # Verifica se o Pokémon inicial compartilha tipos com algum do time
            inicial_type1 = inicial_poke[0][2]
            inicial_type2 = inicial_poke[0][3] if len(inicial_poke[0]) > 3 else None
            type_match = False

            # Verifica se algum tipo do inicial está presente no time
            if (inicial_type1 in poke_chosen_types or
                (inicial_type2 and inicial_type2 in poke_chosen_types)):

                # Procura o primeiro Pokémon no time que compartilha um tipo
                for i in range(len(poke_chosen)):
                    team_poke = poke_chosen[i]
                    team_type1 = team_poke[2]
                    team_type2 = team_poke[3] if len(team_poke) > 3 else None

                    if (inicial_type1 == team_type1 or
                        (inicial_type2 and inicial_type2 == team_type1) or
                        (team_type2 and inicial_type1 == team_type2) or
                        (inicial_type2 and team_type2 and inicial_type2 == team_type2)):

                        poke_chosen[i] = inicial_poke[0]  # Substitui o primeiro compatível
                        type_match = True
                        break

            # Se não compartilha tipos, substitui o mais fraco (menor Total)
            if not type_match:
                for i in range(len(poke_chosen)):
                    if poke_chosen[i][4] < weakest[0]:  # Assumindo que Total está no índice 4
                        weakest[0] = poke_chosen[i][4]
                        weakest[1] = i

                if weakest[1] != -1:  # Se encontrou um Pokémon para substituir
                    poke_chosen[weakest[1]] = inicial_poke[0]

    return poke_chosen


def get_recommended_pokemons(tipos_ideais, poke_starters, db_path="pokemon.db"):
    """
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders_tipo = ','.join(['?'] * len(tipos_ideais))
    placeholders_starters = ','.join(['?'] * len(poke_starters))

    query = f'''
        SELECT *
        FROM Pokemons
        WHERE Legendary = False
          AND Mythical = False
          AND ("Type 1" IN ({placeholders_tipo}) OR "Type 2" IN ({placeholders_tipo}))
          AND entry_number NOT IN ({placeholders_starters})
        ORDER BY Total DESC
    '''

    params = tipos_ideais + tipos_ideais + list(poke_starters)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()


    return rows


def get_names(poke_chosen):
  poke_team = []
  for i in range(len(poke_chosen)):
    poke_team.append(poke_chosen[i][0])

  return poke_team


def show_time(df, time, path_imagens, show_images=True,text ="SEU TIME POKÉMON"):
    st.write("\n" + "===" * 40)
    st.subheader(f"{text}".center(40))
    st.write("===" * 40 + "\n")

    time_df = df.filter(df['Name'].isin(time))

    if time_df.count() == 0:
        print("Nenhum Pokémon no time atual.")
        return []

    nomes_validos = []
    left, right  = st.columns(2,vertical_alignment="bottom")


    for row in time_df.collect():
        nome = row['Name']
        tipos = f"{row['Type 1']}" + (f"/{row['Type 2']}" if row['Type 2'] else "")
        total_stats = row['Total']
        imagem = row['Image']
        nomes_validos.append(nome.lower())

        with left:
            if show_images:
                show_photo([imagem], path_imagens)
                st.write("-" * 30)

        with right:
            st.write(f"Pokémon: {nome}")
            st.write(f"Tipos: {tipos}")
            st.write(f"Status Total: {total_stats}")
            st.write("-" * 30)
        


    return nomes_validos


def get_other_options(poke_chosen, poke_starters, db_path="pokemon.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Extrair dados
    chosen_names = [str(p[0]) for p in poke_chosen]  # Ensure strings
    totals = [p[4] for p in poke_chosen]
    types_1 = [p[2] for p in poke_chosen]
    types_2 = [p[3] for p in poke_chosen]
    all_types = list(set([t for t in types_1 + types_2 if t]))  # Remove tipos None/vazios

    # Build query parts dynamically
    query_parts = []
    params = []

    # Base conditions
    query_parts.append("Total BETWEEN ? AND ?")
    params.extend([min(totals), max(totals)])

    # Type conditions
    if all_types:
        type_conditions = []
        type_conditions.append(f'"Type 1" IN ({",".join("?" for _ in all_types)})')
        type_conditions.append(f'"Type 2" IN ({",".join("?" for _ in all_types)})')
        query_parts.append(f"({' OR '.join(type_conditions)})")
        params.extend(all_types * 2)

    # Starters exclusion
    if poke_starters:
        query_parts.append(f"entry_number NOT IN ({','.join('?' for _ in poke_starters)})")
        params.extend(poke_starters)

    # Chosen names exclusion
    if chosen_names:
        query_parts.append(f"Name NOT IN ({','.join('?' for _ in chosen_names)})")
        params.extend(chosen_names)

    # Build final query
    query = f'''
        SELECT Name, Total, "Type 1", "Type 2"
        FROM Pokemons
        WHERE {' AND '.join(query_parts)}
        ORDER BY  "Type 1",Total DESC
    '''

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        rows = []
    finally:
        conn.close()

    return rows