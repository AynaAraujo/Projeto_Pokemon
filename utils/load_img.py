import os
import streamlit as st
from PIL import Image
from IPython.display import display


def show_photo(poke_fotos, path_imagens):
    for foto in poke_fotos:
        nome_arquivo = foto.replace('images/', '')  # Garante que só o nome do arquivo seja usado
        caminho_completo = os.path.join(path_imagens, nome_arquivo)

        try:
            img = Image.open(caminho_completo)
            st.image(img)
        except FileNotFoundError:
            st.warning(f"Arquivo não encontrado: {caminho_completo}")
        except Exception as e:
            st.warning(f"Erro ao abrir a imagem {caminho_completo}: {str(e)}")
