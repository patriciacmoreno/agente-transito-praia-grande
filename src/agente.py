"""
Lógica do agente Vetor - Mobilidade Urbana de Praia Grande.

Carrega os 7 CSVs de trânsito/mobilidade e monta o contexto relevante
para cada pergunta antes de enviar ao modelo Gemini (Google), que tem
uso gratuito de texto na camada "Free Tier" da API.
"""

import os
import pandas as pd
import google.generativeai as genai

# Pasta onde ficam os CSVs (um nível acima de src/)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Modelo gratuito recomendado (verifique sempre a página de preços do Gemini
# para confirmar quais modelos estão na camada gratuita no momento)
MODELO_GEMINI = "gemini-2.0-flash"

# Cada fonte tem: nome exato do arquivo, encoding correto e uma descrição curta
FONTES = {
    "acidentes_ano": {
        "arquivo": "Acidentes por Bairro e por Ano_Praia Grande.csv",
        "encoding": "cp1252",
        "descricao": "Acidentes de trânsito por bairro, por ano",
    },
    "acidentes_mes": {
        "arquivo": "Acidentes Bairro Mês.csv",
        "encoding": "cp1252",
        "descricao": "Acidentes de trânsito por bairro, por mês",
    },
    "indice_acidentes": {
        "arquivo": "Índice de Acidentes_Praia Grande.csv",
        "encoding": "cp1252",
        "descricao": "Indicadores agregados de acidentes (por habitante, por frota, fatalidade)",
    },
    "frota": {
        "arquivo": "Frota de veiculos por tipo_PG_RMBS.csv",
        "encoding": "cp1252",
        "descricao": "Frota de veículos por tipo, em Praia Grande e municípios da RMBS",
    },
    "transporte": {
        "arquivo": "Transporte intermunicipal.csv",
        "encoding": "cp1252",
        "descricao": "Linhas, frota operacional e passageiros do transporte coletivo intermunicipal",
    },
    "ciclovias": {
        "arquivo": "Infraestrutura cicloviária_Praia Grande.csv",
        "encoding": "utf-8",
        "descricao": "Extensão de ciclovias e ciclofaixas por ano",
    },
    "vias": {
        "arquivo": "Tipo de vias_Praia Grande.csv",
        "encoding": "utf-8",
        "descricao": "Extensão de tipos de vias do município por ano",
    },
}

# Palavras-chave simples para identificar qual(is) tabela(s) a pergunta provavelmente precisa
PALAVRAS_CHAVE = {
    "acidentes_ano": ["acidente", "sinistro"],
    "acidentes_mes": ["mês", "mes", "mensal"],
    "indice_acidentes": ["índice", "indice", "taxa", "habitante", "fatalidade"],
    "frota": ["frota", "veículo", "veiculo", "carro", "moto"],
    "transporte": ["ônibus", "onibus", "transporte coletivo", "passageiro", "linha"],
    "ciclovias": ["ciclovia", "ciclofaixa", "bicicleta", "ciclista"],
    "vias": ["via", "pavimenta", "rua", "avenida"],
}

SYSTEM_PROMPT_BASE = """Você é o Vetor, um agente especializado em dados de trânsito e mobilidade urbana de Praia Grande e da Região Metropolitana da Baixada Santista (RMBS).

Seu objetivo é ajudar cidadãos, jornalistas, pesquisadores e gestores públicos a entender indicadores de segurança viária, transporte coletivo, frota de veículos e infraestrutura viária do município, com base em dados públicos oficiais do Portal de Dados Abertos da Prefeitura de Praia Grande.

BASE DE CONHECIMENTO DISPONÍVEL:
{indice_fontes}

REGRAS:
1. Sempre baseie suas respostas exclusivamente nos dados fornecidos no contexto desta conversa. Nunca invente, estime ou complete números que não estejam explicitamente nos dados.
2. Toda resposta com um número deve citar o ano e o arquivo/fonte de origem.
3. Se o dado perguntado não existir no contexto fornecido, admita claramente que não tem essa informação.
4. Nunca faça previsões futuras nem atribua causas a variações nos números.
5. Nunca emita opinião sobre a gestão pública municipal - apresente os dados de forma neutra.
6. Se a pergunta for fora do escopo de trânsito/mobilidade de Praia Grande e RMBS, informe sua limitação educadamente.
7. Use linguagem acessível, mas precisa: explicite unidades e período dos dados.
"""


def carregar_dados():
    """Carrega todos os CSVs em um dicionário de DataFrames (pandas)."""
    dados = {}
    for chave, info in FONTES.items():
        caminho = os.path.join(DATA_DIR, info["arquivo"])
        dados[chave] = pd.read_csv(caminho, sep=";", encoding=info["encoding"])
    return dados


def montar_indice_fontes():
    """Monta a lista de fontes disponíveis, usada dentro do system prompt."""
    return "\n".join(f"- {info['arquivo']}: {info['descricao']}" for info in FONTES.values())


def identificar_fontes_relevantes(pergunta: str):
    """Identifica, por palavras-chave, quais tabelas provavelmente respondem à pergunta."""
    pergunta_lower = pergunta.lower()
    relevantes = [
        chave for chave, palavras in PALAVRAS_CHAVE.items()
        if any(p in pergunta_lower for p in palavras)
    ]
    # Se nenhuma palavra-chave bater, envia todas as fontes e deixa o modelo decidir
    return relevantes if relevantes else list(FONTES.keys())


def montar_contexto(pergunta: str, dados: dict) -> str:
    """Monta um recorte em texto dos dados relevantes para a pergunta."""
    blocos = []
    for chave in identificar_fontes_relevantes(pergunta):
        df = dados[chave]
        amostra = df.head(50).to_csv(index=False, sep=";")
        blocos.append(f"Fonte: {FONTES[chave]['arquivo']}\n{amostra}")
    return "\n\n".join(blocos)


def montar_system_prompt():
    return SYSTEM_PROMPT_BASE.format(indice_fontes=montar_indice_fontes())


def converter_historico(mensagens):
    """Converte o histórico do Streamlit (role: user/assistant) para o formato do Gemini (role: user/model)."""
    convertido = []
    for msg in mensagens:
        papel = "model" if msg["role"] == "assistant" else "user"
        convertido.append({"role": papel, "parts": [msg["content"]]})
    return convertido


def perguntar_ao_agente(pergunta: str, dados: dict, api_key: str, historico=None) -> str:
    """Envia a pergunta + contexto relevante para o Gemini e retorna a resposta em texto."""
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=MODELO_GEMINI,
        system_instruction=montar_system_prompt(),
    )

    contexto = montar_contexto(pergunta, dados)
    mensagem_usuario = (
        f"Dados disponíveis para responder:\n\n{contexto}\n\nPergunta do usuário: {pergunta}"
    )

    chat = model.start_chat(history=converter_historico(historico or []))
    resposta = chat.send_message(mensagem_usuario)

    return resposta.text
