
# 🧠 Recomendador de Time Pokémon

Um projeto interativo desenvolvido com **Streamlit**, **PySpark** e **Pandas**, que recomenda times de Pokémon baseados no **jogo escolhido** e no **Pokémon inicial selecionado**.

---

## 📌 Funcionalidades

- 🧬 Escolha entre diversas gerações de jogos Pokémon.
- 🔍 Veja qual é o seu Pokémon inicial disponível no jogo.
- 🧠 Receba sugestões de times equilibrados, considerando:
  - Tipos primários e secundários
  - Diversidade tática
  - Pokémon usados por líderes de ginásio
- 📊 Visualize gráficos com a distribuição dos tipos no time.
- 🖼️ (Opcional) Visualize sprites dos Pokémon sugeridos.

---

## ▶️ Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/AynaAraujo/projeto-pokemon.git
cd projeto-pokemon
```

2. Instale os pacotes:
```bash
pip install -r requirements.txt
```

3. Rode o Streamlit:
```bash
streamlit run app.py
```

---

## 📚 Requisitos

- Python 3.8+
- Streamlit
- PySpark
- Pandas

---

## 🧪 Exemplos de Uso

- **Entrada**: `Jogo: Ruby`, `Inicial: Treecko`
- **Saída**:
  - Sugestão de time: Flygon, Aggron, Walrein, Torkoal, Sableye, Manectric
  - Tipos presentes: Water, Ice, Fire, Dragon, Steel

---

## 📖 Fontes

https://pokeapi.co
https://www.kaggle.com/datasets/maxiboo/pokemon-gen-1-9-gym-leaders-elite-four?resource=download
https://www.kaggle.com/datasets/christofferms/pokemon-with-stats-and-image?resource=download
https://www.kaggle.com/datasets/jadenbailey/pokemon-type-chart


---

