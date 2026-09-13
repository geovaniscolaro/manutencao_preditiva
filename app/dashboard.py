import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# Configuração da página
# --------------------------------------------------

st.set_page_config(
    page_title="PoC - Manutenção Preditiva",
    page_icon="⚙️",
    layout="wide"
)

# --------------------------------------------------
# Carregamento
# --------------------------------------------------

@st.cache_resource
def carregar_modelo():
    return joblib.load("modelo_final.joblib")


@st.cache_data
def carregar_dados():
    return pd.read_csv("demo_data.csv")


modelo = carregar_modelo()
dados = carregar_dados()

# --------------------------------------------------
# Cabeçalho
# --------------------------------------------------

st.title("⚙️ Manutenção Preditiva com Inteligência Artificial")

st.write(
    """
    Demonstração de uma Prova de Conceito para classificação
    de estados operacionais de uma máquina industrial a partir
    de dados multissensoriais.
    """
)

st.info(
    "Modelo: HistGradientBoosting | "
    "Sensores: 1, 2 e 3 | "
    "Representação: características temporais + FFT detalhada"
)

# --------------------------------------------------
# Seleção da observação
# --------------------------------------------------

st.subheader("Seleção da observação")

indice = st.slider(
    "Escolha uma observação do conjunto demonstrativo:",
    min_value=0,
    max_value=len(dados) - 1,
    value=0
)

linha = dados.iloc[[indice]]

classe_real = linha["classe_real"].iloc[0]

X = linha.drop(columns=["classe_real"])

# --------------------------------------------------
# Inferência
# --------------------------------------------------

classe_prevista = modelo.predict(X)[0]

probabilidades = modelo.predict_proba(X)[0]

classes_modelo = modelo.classes_

confianca = probabilidades.max()

# --------------------------------------------------
# Resultado
# --------------------------------------------------

st.subheader("Resultado da inferência")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Classe real",
        classe_real
    )

with col2:
    st.metric(
        "Classe prevista",
        classe_prevista
    )

with col3:
    st.metric(
        "Confiança",
        f"{confianca * 100:.2f}%"
    )

if classe_real == classe_prevista:
    st.success("Classificação correta.")
else:
    st.warning("A classificação desta observação foi incorreta.")

# --------------------------------------------------
# Probabilidades
# --------------------------------------------------

st.subheader("Probabilidade estimada por classe")

df_prob = pd.DataFrame(
    {
        "Classe": classes_modelo,
        "Probabilidade": probabilidades
    }
)

df_prob["Probabilidade (%)"] = (
    df_prob["Probabilidade"] * 100
).round(2)

df_prob = df_prob.set_index("Classe")

st.bar_chart(
    df_prob["Probabilidade"]
)

st.dataframe(
    df_prob[["Probabilidade (%)"]],
    use_container_width=True
)

# --------------------------------------------------
# Informações técnicas
# --------------------------------------------------

st.subheader("Informações da PoC")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Número de atributos",
        modelo.n_features_in_
    )

with col5:
    st.metric(
        "Accuracy no holdout",
        "95,13%"
    )

with col6:
    st.metric(
        "Macro F1",
        "95,13%"
    )

st.write(
    """
    A solução final utiliza os Sensores 1, 2 e 3 e combina
    características temporais com informações espectrais obtidas
    por FFT.

    O classificador final utiliza HistGradientBoosting.

    O desempenho de 95,13% foi obtido sobre o conjunto de teste
    estratificado completo com 10.000 observações.

    A interface utiliza uma amostra de 100 observações apenas para
    fins demonstrativos.
    """
)

# --------------------------------------------------
# Limitações
# --------------------------------------------------

st.subheader("Limitações e evolução para produção")

st.write(
    """
    Esta aplicação representa uma Prova de Conceito.

    Para implantação industrial, a solução deverá evoluir com:

    - integração com a plataforma de dados da planta;
    - monitoramento da qualidade dos sensores;
    - validação com máquinas e períodos independentes;
    - API de inferência;
    - monitoramento de desempenho e drift;
    - versionamento de dados e modelos;
    - política de re-treinamento;
    - integração com sistemas de manutenção.
    """
)
