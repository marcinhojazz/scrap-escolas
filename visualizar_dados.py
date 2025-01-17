import streamlit as st
import pandas as pd
import json
import requests

# URL base do repositório GitHub contendo os arquivos JSON
GITHUB_BASE_URL = "https://raw.githubusercontent.com/marcinhojazz/scrap-escolas/main/todas_escolas"

# Função para baixar e carregar os arquivos JSON
@st.cache_data
def load_data_from_github():
    estados = [
    "rondonia.json", "alagoas.json", "acre.json", "espirito-santo.json", "amazonas.json", 
    "goias.json", "mato-grosso-do-sul.json", "roraima.json", "bahia.json", "pernambuco.json", 
    "tocantins.json", "minas-gerais.json", "rio-de-janeiro.json", "distrito-federal.json", 
    "sao-paulo.json", "piaui.json", "mato-grosso.json", "para.json", "paraiba.json", 
    "maranhao.json", "amapa.json", "santa-catarina.json", "ceara.json", "rio-grande-do-sul.json", 
    "parana.json", "rio-grande-do-norte.json", "sergipe.json"
    ]
    
    all_schools = []

    for estado in estados:
        url = f"{GITHUB_BASE_URL}/{estado}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
            data = json.loads(response.text)

            # Processa os dados
            for state, cities in data.items():
                for city, schools in cities.items():
                    for school in schools:
                        all_schools.append({
                            "id": school.get("id"),
                            "name": school.get("name"),
                            "city": city,
                            "state": state,
                            "address": school.get("address", {}).get("street", ""),
                            "phone": school.get("contact", {}).get("full_phone", "")
                        })

        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao carregar dados do arquivo {estado}: {e}")

    return pd.DataFrame(all_schools)

# Visualizar os dados
st.title("Visualização de Dados Escolares Consolidada")
df = load_data_from_github()

# Mostrar uma tabela completa ou filtrada
if not df.empty:
    state_filter = st.selectbox("Selecione o estado", ["Todos"] + df["state"].unique().tolist())
    if state_filter != "Todos":
        df = df[df["state"] == state_filter]

    st.dataframe(df)

    st.download_button(
        label="Baixar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"escolas_{state_filter if state_filter != 'Todos' else 'todas'}.csv",
        mime="text/csv"
    )
else:
    st.warning("Nenhum dado encontrado.")
