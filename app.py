import streamlit as st

# Título da página
st.title("📦 Contador de Produção")

# Inicializa os contadores na sessão
if "total_produzido" not in st.session_state:
    st.session_state.total_produzido = 0

# Botões
if st.button("➕ Registrar Produção"):
    st.session_state.total_produzido += 1
    st.success(f"Produção registrada! Total: {st.session_state.total_produzido}")

if st.button("🔄 Resetar Contador"):
    st.session_state.total_produzido = 0
    st.warning("Contador resetado!")

# Exibe o total produzido
st.metric("📊 Total Produzido", st.session_state.total_produzido)
