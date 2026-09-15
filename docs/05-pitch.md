# Pitch (3 minutos)

## Roteiro

### 1. O Problema (30 seg)

Dados públicos de trânsito e mobilidade de Praia Grande existem, mas estão espalhados em dezenas de planilhas no Portal de Dados Abertos da Prefeitura: acidentes, frota de veículos, transporte coletivo, ciclovias, cada um em um arquivo separado. Um cidadão, jornalista ou pesquisador que queira entender a evolução da segurança viária do seu bairro precisa abrir e cruzar várias dessas planilhas manualmente. Isso torna a informação pública tecnicamente acessível, mas praticamente difícil de usar.

### 2. A Solução (1 min)

O Vetor é um agente de inteligência artificial que conversa em linguagem natural sobre trânsito e mobilidade urbana de Praia Grande e da Região Metropolitana da Baixada Santista. Ele consulta sete bases de dados públicas oficiais (acidentes por bairro e por ano, acidentes por mês, índices de segurança viária, frota de veículos, transporte coletivo intermunicipal, infraestrutura cicloviária e tipos de vias) e responde perguntas como "quantos acidentes aconteceram no meu bairro em 2023?" ou "como está a frota de veículos da cidade?".

O mais importante: o Vetor nunca inventa números. Toda resposta cita a fonte e o ano exatos dos dados. Quando uma informação não existe na base, ele admite isso claramente, em vez de estimar. Ele também se recusa a fazer previsões futuras ou emitir opiniões sobre gestão pública. O papel dele é apresentar os dados de forma neutra, para que cada pessoa possa tirar suas próprias conclusões.

### 3. Demonstração (1 min)

*(Gravação de tela mostrando o chat do Vetor rodando no navegador)*

Mostrar, em sequência:
1. Uma pergunta simples de consulta direta (ex: "Quantos acidentes aconteceram em algum bairro em 2023?") e a resposta organizada, citando a fonte;
2. Uma pergunta que cruza duas bases diferentes (ex: frota de veículos e acidentes), mostrando como o agente apresenta os dois números sem inventar uma relação de causa entre eles;
3. Uma pergunta fora do escopo (ex: "qual a previsão do tempo?") ou pedindo uma previsão futura, mostrando o agente recusando educadamente — prova de que ele não alucina nem extrapola.

### 4. Diferencial e Impacto (30 seg)

O Vetor foi construído inteiramente com ferramentas gratuitas: dados públicos oficiais da prefeitura, a API gratuita do Gemini (Google) e hospedagem no Streamlit Community Cloud — sem custo de infraestrutura. Isso o torna um modelo replicável para outros municípios que também têm portais de dados abertos, mas cuja população não tem como explorá-los sem conhecimento técnico. O impacto real é democratizar o acesso à informação pública: transformar planilhas técnicas em respostas diretas, confiáveis e sempre rastreáveis até a fonte oficial.

---

## Checklist do Pitch

- [x] Duração máxima de 3 minutos
- [x] Problema claramente definido
- [x] Solução demonstrada na prática
- [x] Diferencial explicado
- [x] Áudio e vídeo com boa qualidade

---

## Link do Vídeo

https://youtu.be/8t3Le_9VnDI
