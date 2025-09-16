import streamlit as st
import requests
import pandas as pd
import datetime

# URL da API FastAPI
API_URL = "http://localhost:8000"

# Configuração da página
st.set_page_config(page_title="Viage+", layout="wide")
st.title("🌍 Viage+ : Planejamento de Viagem Inteligente")

# Sidebar para nova busca
st.sidebar.header("Nova busca")
user_id = st.sidebar.number_input("ID do usuário", min_value=1000, value=1001)
origin = st.sidebar.text_input("Cidade Origem", "São Paulo")
destination = st.sidebar.text_input("Destino", "Campinas")
price = st.sidebar.number_input("Preço máximo (R$)", min_value=50, value=150)
alert = st.sidebar.checkbox("Ativar alerta de preço", value=True)

if st.sidebar.button("Enviar busca"):
    # Montar payload compatível com FastAPI
    payload = {
        "user_id": user_id,
        "data": datetime.datetime.now().isoformat(),
        "cidade_origem": origin,  # corresponde ao campo no FastAPI
        "destino": destination,
        "intencao_viagem_data": (datetime.datetime.now() + datetime.timedelta(days=10)).isoformat(),
        "preco": price,
        "alerta": 1 if alert else 0
    }

    # Enviar POST para FastAPI
    try:
        r = requests.post(f"{API_URL}/events/search", json=payload)
        if r.status_code == 200:
            st.success("Busca registrada com sucesso!")
        else:
            st.error(f"Erro: {r.json()}")
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível conectar ao servidor FastAPI: {e}")

# Separador
st.markdown("---")
st.subheader("📊 Estatísticas de Viagem")

# Carregar datasets gerados pelo ETL (mock)
try:
    top_routes = pd.read_csv("data/dashboard_top_rotas.csv")
    st.write("🚌 Rotas mais buscadas:")
    st.bar_chart(top_routes.set_index(["cidade_origem","destino"]).head(10))
except FileNotFoundError:
    st.info("Rode o ETL primeiro para ver estatísticas.")
