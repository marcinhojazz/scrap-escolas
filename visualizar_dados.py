import streamlit as st
import pandas as pd
import json
import os

# Função para carregar dados de um único estado/cidade
@st.cache_data
def load_state_data(state_name, folder_path="todas_escolas"):
    file_path = os.path.join(folder_path, f"{state_name}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame([
            {
                "id": school.get("id"),
                "name": school.get("name"),
                "city": city,
                "state": state_name,
                "address": school.get("address", {}).get("street", ""),
                "phone": school.get("contact", {}).get("full_phone", "")
            }
            for city, schools in data.items()
            for school in schools
        ])
    else:
        st.error(f"Arquivo para {state_name} não encontrado!")
        return pd.DataFrame()

# Interface do Streamlit
st.title("Visualização de Dados Escolares por Estado")

# Lista de estados disponíveis (baseada nos arquivos JSON disponíveis)
states_available = [
    file.replace(".json", "")
    for file in os.listdir("todas_escolas")
    if file.endswith(".json")
]

# Seleção de estado
selected_state = st.selectbox("Selecione o estado", states_available)

# Carregar e exibir dados do estado selecionado
if selected_state:
    df = load_state_data(selected_state)
    if not df.empty:
        st.dataframe(df)

        # Botão para baixar os dados filtrados
        st.download_button(
            label="Baixar CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"escolas_{selected_state}.csv",
            mime="text/csv",
        )
    else:
        st.warning(f"Nenhum dado disponível para o estado: {selected_state}")
