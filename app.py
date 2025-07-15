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
    # Atualiza se já existe, senão insere
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

# Busca opções dinâmicas do banco (level1 e level2)
def get_level_options():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT level2, level1
        FROM sales
        WHERE level1 IS NOT NULL AND level2 IS NOT NULL
        GROUP BY level2, level1
        ORDER BY level2, level1;
    """)
    data = cur.fetchall()
    conn.close()
    return data

# Streamlit app
st.title("📦 Painel de Produção")

# Carregar opções de botões
level_options = get_level_options()

# Agrupar por level2
from collections import defaultdict
grouped_options = defaultdict(list)
for level2, level1 in level_options:
    grouped_options[level2].append(level1)

# Criar botões dinâmicos agrupados
for level2, level1_list in grouped_options.items():
    st.subheader(f"📂 {level2}")  # Título da categoria (level2)
    cols = st.columns(3)  # 3 botões por linha
    for idx, level1 in enumerate(level1_list):
        with cols[idx % 3]:
            if st.button(f"➕ {level1}"):
                incrementar_producao(level1)
                st.success(f"✅ {level1} registrado!")

# Exibir totais
st.subheader("📊 Totais Produzidos:")
for produto, quantidade in get_producao():
    st.metric(label=produto, value=quantidade)
