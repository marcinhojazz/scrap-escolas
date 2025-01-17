import streamlit as st
import pandas as pd
import requests
import json

# Lista de arquivos JSON no repositório
json_files = [
    "acre.json", "alagoas.json", "amapa.json", "amazonas.json", "bahia.json",
    "ceara.json", "distrito-federal.json", "espirito-santo.json", "goias.json",
    "maranhao.json", "mato-grosso-do-sul.json", "mato-grosso.json",
    "minas-gerais.json", "para.json", "paraiba.json", "parana.json",
    "pernambuco.json", "piaui.json", "rio-de-janeiro.json",
    "rio-grande-do-norte.json", "rio-grande-do-sul.json", "rondonia.json",
    "roraima.json", "santa-catarina.json", "sao-paulo.json", "sergipe.json",
    "tocantins.json"
]

# URL base do repositório GitHub
base_url = "https://raw.githubusercontent.com/marcinhojazz/scrap-escolas/main/todas_escolas/"

@st.cache_data
def load_data_from_github():
    all_schools = []

    for file_name in json_files:
        url = f"{base_url}{file_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Processar os dados
            for city, schools in data.items():
                if isinstance(schools, list):  # Certificar-se de que o valor é uma lista
                    for school in schools:
                        all_schools.append({
                            "id": school.get("id"),
                            "name": school.get("name"),
                            "city": city,
                            "state": file_name.replace(".json", ""),
                            "address": school.get("address", {}).get("street", ""),
                            "phone": school.get("contact", {}).get("full_phone", "")
                        })
        except Exception as e:
            st.error(f"Erro ao carregar {file_name}: {e}")

    return pd.DataFrame(all_schools)

# Visualizar os dados
st.title("Visualização de Dados Escolares Consolidada")
df = load_data_from_github()

if not df.empty:
    # Filtro por estado
    state_filter = st.selectbox("Selecione o estado", ["Todos"] + df["state"].unique().tolist())
    if state_filter != "Todos":
        df = df[df["state"] == state_filter]

    # Exibir dados
    st.dataframe(df)

    # Opção de download
    st.download_button(
        label="Baixar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"escolas_{state_filter if state_filter != 'Todos' else 'todas'}.csv",
        mime="text/csv"
    )
else:
    st.warning("Nenhum dado encontrado.")
