import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Conversor de Datas", page_icon="🕓", layout="centered")

st.title("🕓 Conversor de Datas - CSV")
st.write("Envie um arquivo CSV contendo uma coluna de datas no formato `6/30/2025 23:52:07` para converter para o formato `2025-06-30`.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("📤 Envie seu arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Lê o CSV
        df = pd.read_csv(uploaded_file)

        st.subheader("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Escolhe a coluna de data
        colunas = df.columns.tolist()
        coluna_data = st.selectbox("📅 Selecione a coluna de data:", colunas)

        if st.button("🚀 Converter Datas"):
            # Converte a coluna
            df[coluna_data] = pd.to_datetime(df[coluna_data], errors='coerce', format='%m/%d/%Y %H:%M:%S')
            df[coluna_data] = df[coluna_data].dt.strftime('%Y-%m-%d')

            st.success("✅ Conversão concluída com sucesso!")
            st.dataframe(df.head())

            # Opção para baixar o arquivo convertido
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            st.download_button(
                label="⬇️ Baixar CSV Convertido",
                data=buffer,
                file_name="datas_convertidas.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
