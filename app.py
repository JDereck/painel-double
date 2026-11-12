import requests
import pandas as pd
import streamlit as st

API_URL = "https://blitz4.casino/api/singleplayer-originals/originals/roulette_games/recent/1"

def buscar_dados():
    """Busca os dados da API ao vivo com cabeçalho de navegador"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        # Mostra o status na tela para sabermos se a API respondeu
        st.info(f"Status da Conexão com a API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"A API recusou a conexão. Resposta: {response.text}")
    except Exception as e:
        st.error(f"Erro técnico ao conectar: {e}")
    return []

# --- Interface Streamlit ---
st.title("🎯 Painel Analisador de Branco - Double")
st.subheader("Monitoramento em Tempo Real")

if st.button("🔄 Atualizar Dados Agora"):
    st.rerun()

dados = buscar_dados()

if dados:
    st.success(f"Conexão bem-sucedida! {len(dados)} rodadas carregadas.")
    df = pd.DataFrame(dados)
    
    # Exibe a tabela com os dados brutos da API
    st.dataframe(df, use_container_width=True)
else:
    st.warning("Aguardando dados válidos da API...")
