import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Dashboard - Crescimento Demográfico", layout="wide"
)

st.title("🏙️ Análise de Crescimento Demográfico e Cidades Outliers")
st.markdown(
    "Módulo individual voltado para o apoio aos Prefeitos de Capitais na revisão de Planos Diretores."
)


@st.cache_data
def carregar_dados():
    np.random.seed(42)
    dados = {
        "Municipio": [
            "Curitiba",
            "Belo Horizonte",
            "Salvador",
            "Porto Alegre",
            "Florianópolis",
            "São Paulo",
            "Rio de Janeiro",
            "Fortaleza",
            "Recife",
            "Manaus",
        ],
        "Regiao": ["Sul", "Sudeste", "Nordeste", "Sul", "Sul", "Sudeste", "Sudeste", "Nordeste", "Nordeste", "Norte"],
        "Taxa_Crescimento_Anual": np.random.normal(1.2, 0.8, 10),
        "Populacao_2022": np.random.randint(500000, 12000000, 10),
    }
    df = pd.DataFrame(dados)
    df.loc[0, "Taxa_Crescimento_Anual"] = 4.5  
    df.loc[3, "Taxa_Crescimento_Anual"] = -1.8  
    return df

df = carregar_dados()


st.sidebar.header("🔍 Filtros de Análise")
regiao_selecionada = st.sidebar.selectbox(
    "Selecione a Região", options=["Todas"] + list(df["Regiao"].unique())
)

if regiao_selecionada != "Todas":
    df_filtrado = df[df["Regiao"] == regiao_selecionada]
else:
    df_filtrado = df


taxas = df_filtrado["Taxa_Crescimento_Anual"]

media = taxas.mean()
mediana = taxas.median()
amplitude = taxas.max() - taxas.min()
desvio_padrao = taxas.std()

# Quartis e IQR
q1 = np.percentile(taxas, 25)
q3 = np.percentile(taxas, 75)
iqr = q3 - q1


limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr
outliers = df_filtrado[
    (taxas < limite_inferior) | (taxas > limite_superior)
]

st.subheader("📊 Métricas Estatísticas do Indicador")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Média", f"{media:.2f}%")
col2.metric("Mediana", f"{mediana:.2f}%")
col3.metric("IQR", f"{iqr:.2f}")
col4.metric("Desvio Padrão", f"{desvio_padrao:.2f}")
col5.metric("Amplitude", f"{amplitude:.2f}%")


st.markdown("---")
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Gráfico de Barras: Crescimento por Cidade")
    st.bar_chart(df_filtrado.set_index("Municipio")["Taxa_Crescimento_Anual"])

with col_g2:
    st.subheader("Análise de Outliers (Cidades Anômalas)")
    if not outliers.empty:
        st.warning(
            "Foram identificadas cidades fora do padrão de normalidade estatística ($1.5 \\times IQR$):"
        )
        st.dataframe(
            outliers[["Municipio", "Regiao", "Taxa_Crescimento_Anual"]]
        )
    else:
        st.success(
            "Não há outliers com base no filtro e na regra estatística aplicada."
        )


st.markdown("---")
st.subheader("📰 Contextualização e Transição Demográfica")
st.markdown(
    """
    > **Resumo Executivo para Gestores:** A análise da dispersão e dos quartis demonstra que a maior parte das capitais 
    > converge para um crescimento estável, enquanto polos específicos sofrem com desvios acentuados devido à expansão urbana 
    > acelerada ou esvaziamento demográfico.
    """
)