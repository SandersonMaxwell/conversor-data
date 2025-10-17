import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Conversor de Datas (Excel)", page_icon="📅", layout="centered")

st.title("📅 Conversor de Datas - Arquivo Excel (.xlsx)")
st.write("Envie um arquivo Excel contendo uma coluna de datas no formato `6/30/2025 23:52:07` para converter para o formato `2025-06-30` (ano-mês-dia).")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("📤 Envie seu arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê o Excel
        df = pd.read_excel(uploaded_file)

        st.subheader("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Seleciona a coluna de data
        colunas = df.columns.tolist()
        coluna_data = st.selectbox("📅 Selecione a coluna de data:", colunas)

        if st.button("🚀 Converter Datas"):
            # Converte a coluna
            df[coluna_data] = pd.to_datetime(df[coluna_data], errors='coerce')
            df[coluna_data] = df[coluna_data].dt.strftime('%Y-%m-%d')

            st.success("✅ Conversão concluída com sucesso!")
            st.dataframe(df.head())

            # Gera arquivo Excel convertido
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, in_
