import streamlit as st
import psycopg2
import os

# Conexão com o banco usando DB_URL
DB_URL = os.getenv("DB_URL")

def get_connection():
    return psycopg2.connect(DB_URL)

# Incrementa produção
def incrementar_producao(produto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantidade FROM producao WHERE produto=%s;", (produto,))
    result = cur.fetchone()
    if result:
        cur.execute("UPDATE producao SET quantidade = quantidade + 1 WHERE produto=%s;", (produto,))
    else:
        cur.execute("INSERT INTO producao (produto, quantidade) VALUES (%s, 1);", (produto,))
    conn.commit()
    conn.close()

# Busca produção total
def get_producao():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT produto, quantidade FROM producao ORDER BY produto;")
    data = cur.fetchall()
    conn.close()
    return data

# Busca opções dinâmicas (level1 e level2) filtrando apenas level2 que contém "STEP"
def get_level_options():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT level2, level1
        FROM sales
        WHERE level1 IS NOT NULL 
          AND level2 ILIKE '%STEP%'
        GROUP BY level2, level1
        ORDER BY level2, level1;
    """)
    data = cur.fetchall()
    conn.close()
    return data

# Streamlit layout estilo painel
st.set_page_config(page_title="Painel de Produção", layout="wide")
st.title("🏭 Painel de Produção - STEP")

# Carregar opções de botões
level_options = get_level_options()

if not level_options:
    st.warning("⚠️ Nenhum produto encontrado para 'STEP' em level2.")
else:
    # Agrupar por level2
    from collections import defaultdict
    grouped_options = defaultdict(list)
    for level2, level1 in level_options:
        grouped_options[level2].append(level1)

    # Estilo customizado
    st.markdown("""
        <style>
        .stButton button {
            font-size: 1.5em;
            padding: 1em;
            width: 100%;
            height: 100px;
            border-radius: 10px;
            font-weight: bold;
        }
        .metric-container {
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Criar botões grandes agrupados por level2
    for level2, level1_list in grouped_options.items():
        st.subheader(f"📂 {level2}")
        cols = st.columns(3)  # 3 botões por linha
        for idx, level1 in enumerate(level1_list):
            with cols[idx % 3]:
                if st.button(f"➕ {level1}"):
                    incrementar_producao(level1)
                    st.success(f"✅ {level1} registrado!")

# Exibir totais com destaque
st.header("📊 Totais Produzidos:")
totais = get_producao()
metric_cols = st.columns(4)
for idx, (produto, quantidade) in enumerate(totais):
    with metric_cols[idx % 4]:
        st.metric(label=f"📦 {produto}", value=quantidade)
