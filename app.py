import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Conversor de Datas (Excel)", page_icon="📅", layout="centered")

st.title("📅 Conversor de Datas - Arquivo Excel (.xlsx)")
st.write("""
Envie um arquivo Excel contendo uma coluna de datas no formato `6/30/2025 23:52:07`.  
O app vai converter para o formato **`YYYY-MM-DD`** (ano-mês-dia) automaticamente.
A coluna de data deve estar na **segunda coluna (coluna B)**.
""")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("📤 Envie seu arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Lê o Excel
        df = pd.read_excel(uploaded_file)

        st.subheader("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Define a coluna de data como coluna B (segunda coluna)
        coluna_data = df.columns[1]

        if st.button("🚀 Converter Datas"):
            # Converte a coluna para datetime
            df[coluna_data] = pd.to_datetime(df[coluna_data], errors='coerce')
            # Formata apenas ano-mês-dia
            df[coluna_data] = df[coluna_data].dt.strftime('%Y-%m-%d')

            st.success("✅ Conversão concluída com sucesso!")
            st.dataframe(df.head())

            # Cria buffer para download do Excel convertido
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados Convertidos')
            buffer.seek(0)

            st.download_button(
                label="⬇️ Baixar Excel Convertido",
                data=buffer,
                file_name="datas_convertidas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao processar o arquivo: {e}")
