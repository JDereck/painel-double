import requests
import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta

# Configurações da API original e uma rota de fallback segura para testes
API_URL = "https://blitz4.casino/api/singleplayer-originals/originals/roulette_games/recent/1"

def buscar_dados():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json(), "API Oficial"
        else:
            # Se a API bloquear por país, geramos dados simulados idênticos para você estruturar o painel
            return gerar_dados_simulados(), "Modo Simulação (Bloqueio Geográfico Contornado)"
    except Exception:
        return gerar_dados_simulados(), "Modo Simulação (Erro de Conexão)"

def gerar_dados_simulados():
    """Gera dados idênticos ao formato da API para testes e desenvolvimento do painel"""
    dados = []
    tempo_atual = datetime.utcnow()
    # Cores: 1 = Vermelho, 2 = Preto, 0 = Branco
    cores_possiveis = [1, 2, 1, 2, 1, 2, 1, 2, 0, 1, 2] # O 0 aparece de vez em quando (Branco)
    
    for i in range(50):
        cor = random.choice(cores_possiveis)
        roll = 0 if cor == 0 else random.randint(1, 7) if cor == 1 else random.randint(8, 14)
        
        dados.append({
            "id": f"sim_{i}",
            "created_at": (tempo_atual - timedelta(seconds=30*i)).isoformat() + "Z",
            "color": cor,
            "roll": roll,
            "server_seed": "simulated_seed_hash"
        })
    return dados

# --- Interface Streamlit ---
st.title("🎯 Painel Analisador de Branco - Double")
st.subheader("Monitoramento e Inteligência de Padrões")

if st.button("🔄 Atualizar Dados Agora"):
    st.rerun()

dados, origem = buscar_dados()

st.info(f"Fonte dos Dados: **{origem}**")

if dados:
    df = pd.DataFrame(dados)
    
    # Tratamento e métricas focadas no BRANCO
    # Considerando 'roll == 0' ou 'color == 0' como Branco
    df['is_branco'] = (df['roll'] == 0) | (df['color'] == 0)
    
    total_rodadas = len(df)
    total_brancos = df['is_branco'].sum()
    
    # Calcular o Gap atual (quantas rodadas faz que não sai o branco)
    # Encontrar a posição do último branco
    brancos_indices = df.index[df['is_branco']].tolist()
    gap_atual = brancos_indices[0] if brancos_indices else total_rodadas
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Rodadas", total_rodadas)
    col2.metric("Brancos no Histórico", total_brancos)
    col3.metric("🔴 Gap Atual (Sem Branco)", f"{gap_atual} jogadas")
    
    st.divider()
    st.subheader("📊 Histórico Recente e Status do Branco")
    
    # Exibir tabela formatada
    st.dataframe(df[['created_at', 'roll', 'color', 'is_branco']], use_container_width=True)
    
else:
    st.warning("Aguardando dados...")
