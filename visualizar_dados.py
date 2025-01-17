import streamlit as st
import pandas as pd
import json
import os
import zipfile

# Descompactar o arquivo ZIP contendo os dados JSON
@st.cache
def extract_data(zip_path="todas_escolas.zip", extract_to="todas_escolas"):
    if not os.path.exists(extract_to):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
    return extract_to

# Carregar todos os dados JSON
@st.cache
def load_all_data(folder_path):
    all_schools = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
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
    return pd.DataFrame(all_schools)

# Visualizar os dados
st.title("Visualização de Dados Escolares Consolidada")

# Extraia os dados antes de carregar
folder_path = extract_data()
df = load_all_data(folder_path)

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
    st.warning("Nenhum dado encontrado na pasta especificada.")
