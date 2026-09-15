# Base de Conhecimento

## Fonte dos Dados

Os dados utilizados pelo agente foram extraídos do **Portal de Dados Abertos da Prefeitura de Praia Grande** (GeoNetwork), disponível em:
https://dadosabertos.praiagrande.sp.gov.br/geonetwork/srv/por/catalog.search#/metadata/0655b320-574a-4b58-922d-c1508cf54592

São dados públicos oficiais do município, cobrindo indicadores de trânsito, transporte coletivo, frota de veículos e infraestrutura viária. Por serem dados abertos governamentais, não há informações pessoais ou sensíveis envolvidas, o que também simplifica a etapa de segurança do agente.

---

## Dados Utilizados

O agente utiliza 7 arquivos CSV extraídos do portal acima, organizados na pasta `data/`:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `Acidentes por Bairro e por Ano_Praia Grande.csv` | CSV | Consultar número de acidentes de trânsito por bairro, ano a ano |
| `Acidentes Bairro Mês.csv` | CSV | Consultar acidentes de trânsito por bairro com granularidade mensal |
| `Índice de Acidentes_Praia Grande.csv` | CSV | Fornecer indicadores agregados: acidentes por 100 mil habitantes, mortes por 10 mil veículos e taxa de fatalidade |
| `Frota de veiculos por tipo_PG_RMBS.csv` | CSV | Consultar a frota de veículos por tipo (carro, moto, caminhão etc.) em Praia Grande e municípios da RMBS |
| `Transporte intermunicipal.csv` | CSV | Consultar linhas, frota operacional e passageiros transportados no transporte coletivo intermunicipal |
| `Infraestrutura cicloviária_Praia Grande.csv` | CSV | Consultar extensão e tipo de infraestrutura cicloviária (ciclovias, ciclofaixas) por ano |
| `Tipo de vias_Praia Grande.csv` | CSV | Consultar a extensão (em metros) dos diferentes tipos de vias do município, por ano |

> [!TIP]
> O mesmo portal disponibiliza outros datasets do município (ex: fluxo de veículos no Sistema Anchieta-Imigrantes, óbitos por causa, veículos cadastrados por habitante). É possível expandir a base do agente incorporando mais arquivos de lá, seguindo a mesma lógica de integração descrita abaixo.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados não foram inventados nem alterados em conteúdo: são exportações diretas do Portal de Dados Abertos de Praia Grande, selecionadas a partir de um conjunto maior de arquivos disponíveis no portal, priorizando os que cobrem as quatro frentes definidas na documentação do agente (segurança viária, frota de veículos, transporte coletivo e infraestrutura viária).

Um ponto técnico de adaptação necessário: os arquivos, como exportados do portal, usam **ponto e vírgula (`;`)** como separador de colunas (em vez de vírgula) e parte deles está em codificação **cp1252** (Windows), não em UTF-8. Isso precisa ser considerado na hora de carregar os dados no código do agente, por exemplo, em Python/pandas:

```python
import pandas as pd

df = pd.read_csv("data/Acidentes por Bairro e por Ano_Praia Grande.csv", sep=";", encoding="cp1252")
```

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os 7 CSVs são carregados no início da sessão da aplicação (com pandas, usando `sep=";"` e o encoding correto para cada arquivo) e mantidos em memória como tabelas separadas. O agente **não** injeta todas as tabelas inteiras no prompt de uma vez, isso ultrapassaria o contexto do modelo rapidamente, já que alguns arquivos têm centenas de linhas (ex: dados por bairro e por mês). Em vez disso, o agente identifica, a partir da pergunta do usuário, qual tabela é relevante e aplica um filtro (por ano, bairro, tipo de via etc.) antes de repassar o recorte de dados ao modelo de linguagem.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

O **system prompt** contém apenas a descrição de quais tabelas existem, o que cada uma representa e a fonte oficial (um "índice" da base de conhecimento, não os dados em si). Os **dados propriamente ditos** são consultados dinamicamente: a cada pergunta do usuário, o agente decide qual arquivo consultar, filtra as linhas relevantes (via pandas) e insere apenas esse recorte no contexto da conversa, junto com uma instrução de que a resposta deve se basear exclusivamente nesse recorte e sempre citar a fonte.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Pergunta do usuário: *"Quantos acidentes aconteceram no bairro Boqueirão em 2023?"*

```
Consulta: Acidentes por Bairro e por Ano_Praia Grande.csv
Filtro aplicado: Bairro = "Boqueirão"

Resultado encontrado:
- Bairro: Boqueirão | Ano: 2021 | Acidentes de Trânsito Por Ano: 143
- Bairro: Boqueirão | Ano: 2022 | Acidentes de Trânsito Por Ano: 128
- Bairro: Boqueirão | Ano: 2023 | Acidentes de Trânsito Por Ano: 135

Fonte: Portal de Dados Abertos de Praia Grande — Acidentes por Bairro e por Ano_Praia Grande.csv
```

*(Os números acima são apenas ilustrativos, para exemplificar o formato — o agente sempre usa os valores reais encontrados no arquivo.)*
