import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Arena de Agentes - Double Branco", layout="wide")

st.title("🧬 Arena Evolutiva: 100 Agentes Buscando o Padrão do Branco")
st.markdown("Cada um dos 100 agentes possui uma regra de entrada diferente. Eles competem usando uma banca inicial de **1000**, e o sistema identifica o melhor indivíduo.")

# --- 1. GERAR OU CARREGAR HISTÓRICO ROBUSTO ---
@st.cache_data
def carregar_historico_gigante():
    """Simula ou carrega um histórico denso para os agentes estudarem"""
    np.random.seed(42)
    tamanho = 10000 # 10 mil rodadas de histórico para estudo profundo
    
    # 0 = Branco, 1 = Vermelho, 2 = Preto
    # Probabilidade realista do branco (~7%)
    cores = np.random.choice([1, 2, 0], size=tamanho, p=[0.465, 0.465, 0.07])
    rolls = [0 if c == 0 else np.random.randint(1, 7) if c == 1 else np.random.randint(8, 14) for c in cores]
    
    df = pd.DataFrame({
        "id": [f"rodada_{i}" for i in range(tamanho)],
        "color": cores,
        "roll": rolls,
        "is_branco": (cores == 0)
    })
    return df

df_historico = carregar_historico_gigante()

st.sidebar.header("⚙️ Configurações da Simulação")
num_agentes = st.sidebar.slider("Número de Agentes Competindo", 50, 200, 100)
banca_inicial = st.sidebar.number_input("Banca Inicial de Cada Agente", value=1000, step=100)
aposta_fixa = st.sidebar.number_input("Valor da Aposta por Jogada no Branco", value=10, step=5)
multiplicador_branco = 14.0 # Pagamento médio do branco

if st.button("🚀 Iniciar Competição e Evolução dos Agentes"):
    
    with st.spinner("Simulando os agentes em cima do histórico... Isso pode levar alguns segundos."):
        
        resultados_agentes = []
        historico_bancas_campeao = []
        
        # Cada agente tem um 'gatilho' diferente (ex: entra quando o gap está entre X e Y)
        for i in range(num_agentes):
            gap_gatilho = random.randint(5, 25) # Estratégia única do agente
            martingale = random.choice([True, False]) # Se usa progressão ou stake fixa
            
            banca = float(banca_inicial)
            historico_banca = [banca]
            acertos = 0
            erros = 0
            aposta_atual = float(aposta_fixa)
            
            # O agente "joga" rodada por rodada no histórico para ver seu desempenho
            gap_atual = 0
            for idx, row in df_historico.iterrows():
                if banca <= 0:
                    break # Agente quebrbrou a banca
                
                is_branco = row['is_branco']
                
                # Verifica se a estratégia do agente diz para apostar nesta rodada
                if gap_atual >= gap_gatilho:
                    # Agente faz a aposta no Branco
                    if banca >= aposta_atual:
                        banca -= aposta_atual
                        if is_branco:
                            ganho = aposta_atual * multiplicador_branco
                            banca += ganho
                            acertos += 1
                            aposta_atual = float(aposta_fixa) # Reseta aposta
                            gap_atual = 0
                        else:
                            erros += 1
                            if martingale:
                                aposta_atual *= 2 # Dobra no erro (arriscado, mas comum)
                    else:
                        break
                
                if is_branco:
                    gap_atual = 0
                else:
                    gap_atual += 1
                
                historico_banca.append(banca)
            
            lucro_final = banca - banca_inicial
            roi = (lucro_final / banca_inicial) * 100
            
            resultados_agentes.append({
                "id_agente": f"Agente #{i+1}",
                "gap_gatilho": gap_gatilho,
                "usa_martingale": martingale,
                "banca_final": banca,
                "lucro": lucro_final,
                "roi": roi,
                "acertos": acertos,
                "erros": erros,
                "historico": historico_banca
            })
        
        # Ordenar agentes pelo melhor resultado financeiro (Banca Final)
        resultados_agentes = sorted(resultados_agentes, key=lambda x: x['banca_final'], reverse=True)
        melhor_agente = resultados_agentes[0]
        
        # --- EXIBIÇÃO DOS RESULTADOS ---
        st.success("🏆 Competição Concluída! O Melhor Indivíduo foi Encontrado.")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Melhor Agente", melhor_agente['id_agente'])
        col2.metric("Banca Final", f"R$ {melhor_agente['banca_final']:.2f}")
        col3.metric("Lucro Obtido", f"R$ {melhor_agente['lucro']:.2f}", f"{melhor_agente['roi']:.1f}% ROI")
        col4.metric("Estratégia (Gap Gatilho)", f"Entra no Gap {melhor_agente['gap_gatilho']}")
        
        st.divider()
        st.subheader("📈 Gráfico de Desempenho do Melhor Indivíduo vs. Média da Arena")
        
        # Gráfico com Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Plota o campeão
        ax.plot(melhor_agente['historico'], label=f"Campeão ({melhor_agente['id_agente']})", color='green', linewidth=2)
        
        # Plota alguns agentes medianos para comparação
        for i in range(1, min(5, len(resultados_agentes))):
            ax.plot(resultados_agentes[i]['historico'], color='gray', alpha=0.3, linestyle='--')
            
        ax.axhline(y=banca_inicial, color='red', linestyle=':', label='Banca Inicial (1000)')
        ax.set_title("Evolução da Banca ao Longo do Histórico")
        ax.set_xlabel("Rodadas simuladas")
        ax.set_ylabel("Valor da Banca (R$)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        st.subheader("📋 Top 5 Agentes Campeões da Arena")
        df_ranking = pd.DataFrame(resultados_agentes)[['id_agente', 'gap_gatilho', 'usa_martingale', 'banca_final', 'lucro', 'acertos', 'erros']].head(5)
        st.dataframe(df_ranking, use_container_width=True)

else:
    st.info("👈 Ajuste os parâmetros na barra lateral e clique no botão para iniciar a evolução dos agentes!")
