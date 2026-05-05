# pipeline-treino-dados
Pipeline ETL: Google Sheets → Python → PostgreSQL → Power BI
# Pipeline de Dados — Monitoramento de Treinos

Pipeline ETL completo para coleta, armazenamento e visualização de dados de treino na academia.

## Arquitetura

Google Sheets → Python (ETL) → PostgreSQL → Power BI

## O que o pipeline faz

- Coleta os registros de treino diretamente do Google Sheets via API
- Aplica tratamento de outliers com IQR para garantir integridade dos dados
- Armazena os dados em um banco PostgreSQL com modelagem dimensional (fato + dimensão)
- Visualiza as métricas no Power BI com atualização sob demanda

## Dashboard

- Volume total movimentado (kg)
- Distribuição de volume por grupo muscular
- Total de séries por grupo muscular
- Evolução da carga máxima ao longo do tempo
- Filtro interativo por período

## Tecnologias

- Python (pandas, psycopg2, gspread)
- PostgreSQL + DBeaver
- Power BI
- Google Sheets API
- Git + GitHub

## Como executar

1. Clone o repositório
2. Crie um arquivo `.env` na raiz com as variáveis:
DB_HOST=localhost
DB_NAME=treinos
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
3. Adicione o arquivo `credenciais.json` da sua conta de serviço do Google
4. Execute o script:

## Estrutura do banco

- `dim_exercicios` — cadastro de exercícios com grupo muscular
- `fato_treino` — registros diários de carga e repetições
