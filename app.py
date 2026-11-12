import requests
import pandas as pd
import streamlit as st
import time

# Configurações da API e Telegram
API_URL = "https://blitz4.casino/api/singleplayer-originals/originals/roulette_games/recent/1"
TELEGRAM_TOKEN = "SEU_TOKEN_DO_BOT_AQUI"
CHAT_ID = "SEU_CHAT_ID_AQUI"

def enviar_alerta_telegram(mensagem):
    """Envia notificação para o Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar telegram: {e}")

def buscar_dados():
    """Busca os dados da API ao vivo"""
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
    return []

# --- Interface Streamlit ---
st.title("🎯 Painel Analisador de Branco - Double")
st.subheader("Monitoramento em Tempo Real e Alertas Automáticos")

if st.button("🔄 Atualizar Dados Agora"):
    st.rerun()

dados = buscar_dados()

if dados:
    df = pd.DataFrame(dados)
    
    # Tratamento básico dos dados
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = df.sort_values('created_at', ascending=False).reset_index(drop=True)
    
    # Exibir métricas rápidas
    total_rodadas = len(df)
    
    # Supondo que o Branco seja identificado por uma cor específica ou roll (ajuste conforme o padrão da API para o branco)
    # Exemplo: se o branco for color == 0 ou roll == 0 (ajuste conforme regra da casa)
    # Vamos criar um filtro simulado para o Branco:
    brancos_recentes = df[df['roll'] == 0] # Ajuste o identificador do branco se necessário
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Analisado (API)", total_rodadas)
    col2.metric("Último Roll", df.iloc[0]['roll'])
    col3.metric("Última Cor", df.iloc[0]['color'])
    
    st.divider()
    st.write("### Histórico Recente de Jogadas")
    st.dataframe(df[['created_at', 'id', 'roll', 'color']], use_container_width=True)
    
    # Lógica de Gatilho para o Branco (Exemplo de Estratégia por Gap)
    # Se há muitas rodadas sem sair o alvo, o script pode avisar
    # (Insira aqui sua lógica matemática ou de machine learning)
    
else:
    st.warning("Aguardando dados da API...")
