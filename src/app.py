"""
Aplicação Streamlit - Chatbot do agente Vetor (Mobilidade Urbana de Praia Grande).
"""

import streamlit as st
from agente import carregar_dados, perguntar_ao_agente
from config import GEMINI_API_KEY

st.set_page_config(page_title="Vetor - Mobilidade Praia Grande", page_icon="🚦")
st.title("🚦 Vetor - Agente de Mobilidade Urbana de Praia Grande")
st.caption("Dados públicos de trânsito, transporte e segurança viária de Praia Grande e RMBS")


@st.cache_data
def get_dados():
    return carregar_dados()


dados = get_dados()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

pergunta = st.chat_input(
    "Pergunte sobre acidentes, frota, ciclovias ou transporte coletivo em Praia Grande..."
)

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando os dados..."):
            resposta = perguntar_ao_agente(
                pergunta,
                dados,
                GEMINI_API_KEY,
                historico=st.session_state.mensagens[:-1],
            )
            st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
