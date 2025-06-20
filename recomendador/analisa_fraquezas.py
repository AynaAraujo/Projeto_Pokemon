import sqlite3
from collections import Counter

def set_first_column_as_index(df):
    """
    Define a primeira coluna de um DataFrame como índice.

    Parâmetros:
    - df: DataFrame do pandas.

    Retorna:
    - O DataFrame com a primeira coluna definida como índice.
    """
    df.set_index(df.columns[0], inplace=True)
    return df


def get_top_effective_types(tipos_selecionados, matriz_dano):
    """
    Retorna os 6 tipos mais eficazes contra os tipos selecionados,
    com base na matriz de dano.

    Parâmetros:
    - tipos_selecionados: Lista de tipos (strings) dos rivais.
    - matriz_dano: DataFrame da matriz de eficácia de tipos (type chart).

    Retorna:
    - Lista com os 6 tipos mais ofensivamente eficazes.
    """
    resultado = []

    for tipo in tipos_selecionados:
        if tipo not in matriz_dano.index:
            raise ValueError(f"Tipo '{tipo}' não encontrado na matriz.")

        # Ordena os tipos defensivos mais vulneráveis a esse tipo ofensivo
        tipos_ordenados = matriz_dano[tipo].sort_values(ascending=False)
        resultado.append((tipo, tipos_ordenados[:2]))

    # Extrair os tipos mais vulneráveis (supereficazes)
    supereficazes = []
    for _, series in resultado:
        supereficazes.extend(series.index.tolist())

    # Contar frequência e extrair os 6 mais comuns
    contagem = Counter(supereficazes)
    tipos_ideais = [tipo for tipo, _ in contagem.most_common(6)]

    return tipos_ideais

