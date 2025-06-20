import requests
from utils.spark_session import spark



def choose_game(game_name):
    game_name = game_name.lower()

    if game_name in ['red', 'fire red', 'blue', 'leaf green']:
        id = 1
    elif game_name in ['gold', 'silver', 'heartgold', 'soulsilver']:
        id = 2
    elif game_name in ['ruby', 'sapphire', 'emerald', 'omega ruby', 'alpha sapphire']:
        id = 3
    elif game_name in ['diamond', 'pearl', 'platinum', 'brilliant diamond', 'shining pearl']:
        id = 4
    elif game_name in ['black', 'white', 'black 2', 'white 2']:
        id = 5
    elif game_name in ['x', 'y']:
        id = 6
    elif game_name in ['sun', 'moon', 'ultra sun', 'ultra moon']:
        id = 7
    elif game_name in ['sword', 'shield']:
        id = 8
    elif game_name in ['scarlet', 'violet']:
        id = 9
    else:
        id = 0  # Caso o jogo não esteja na lista

    print(f"ID do jogo: {id}")
    return id


def pegando_pokedex(idGame):
    """
    Pega os números (National Dex IDs) de todos os Pokémon introduzidos
    na geração especificada por idGame.

    Args:
        idGame (int): O ID da geração (ex: 1 para Kanto, 2 para Johto).

    Returns:
        list: Uma lista de inteiros contendo os IDs dos Pokémon da geração.
    """
    # 1. Pegando dados da geração escolhida
    try:
        url = f'https://pokeapi.co/api/v2/generation/{idGame}/'
        r = requests.get(url)
        r.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        dados_gen = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à PokeAPI para a geração {idGame} na URL {url}: {e}")
        return [] # Retorna uma lista vazia em caso de erro

    # 2. Pegando nome da Região (opcional, para informação)
    region = dados_gen['main_region']['name']
    print(f"Região da Geração: {region.capitalize()}")

    # 3. Extraindo os números (IDs) e os nomes (para o print final) dos Pokémon da geração
    poke_data_for_generation = [] # Para armazenar ID e Nome
    for species_data in dados_gen['pokemon_species']:
        url_parts = species_data['url'].split('/')
        try:
            pokemon_id = int(url_parts[-2])
            poke_data_for_generation.append({
                'id': pokemon_id,
                'name': species_data['name']
            })
        except (ValueError, IndexError):
            print(f"Aviso: Não foi possível extrair o ID para {species_data['name']} da URL: {species_data['url']}")
            continue

    # Ordenar pela ID para garantir consistência
    poke_data_for_generation.sort(key=lambda x: x['id'])

    # Extrai apenas os IDs para o retorno principal da função
    poke_numbers = [item['id'] for item in poke_data_for_generation]

    # 4. Impressões de verificação
    print(f"Total de Pokémon na Geração {idGame}: {len(poke_numbers)}")
    if poke_numbers:
        # Pega o primeiro e último item da lista já ordenada e com nomes
        first_poke = poke_data_for_generation[0]
        last_poke = poke_data_for_generation[-1]

        print(f"Primeiro Pokémon: {first_poke['name'].capitalize()} (Nº {first_poke['id']})")
        print(f"Último Pokémon: {last_poke['name'].capitalize()} (Nº {last_poke['id']})")
    else:
        print("Nenhum Pokémon encontrado para esta geração.")

    return poke_numbers


def criar_df(path,sep = ","):

  df = spark.read.csv(path,
                      escape="\"",
                      header=True,
                      inferSchema=True,
                      sep=sep,
                      encoding="utf-8")
  return df



