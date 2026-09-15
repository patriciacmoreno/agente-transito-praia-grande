"""
Configurações do agente Vetor.

A chave da API do Gemini fica guardada nos "Secrets" do Streamlit
(no Streamlit Community Cloud: Settings > Secrets do seu app) e nunca
deve ser escrita diretamente aqui no código nem commitada no GitHub.

Para gerar uma chave gratuita: https://aistudio.google.com/apikey
"""

import streamlit as st

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
