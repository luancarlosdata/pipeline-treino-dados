import pandas as pd
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

load_dotenv()

# 1. ACESSO
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
client = gspread.authorize(creds)

spreadsheet_name = 'projeto-treino'
sheet = client.open(spreadsheet_name).get_worksheet(1)

# 2. CARREGAR DADOS DA PLANILHA
data = sheet.get_all_records()
df = pd.DataFrame(data)
print(f"Dados lidos: {len(df)} linhas.")

# 3. TRATAMENTO DE OUTLIERS
Q1 = df['KG'].quantile(0.25)
Q3 = df['KG'].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR

df_limpo = df[df['KG'] <= limite_superior]
print(f"Dados após limpeza de outliers: {len(df_limpo)} linhas.")

# 4. CONEXÃO COM O BANCO DE DADOS
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    # 5. CARGA NO BANCO DE DADOS (UPSERT)
    for index, row in df_limpo.iterrows():
        nome_exercicio = str(row['EXERCICIO']).strip().lower()

        cursor.execute("SELECT id_exercicio FROM dim_exercicios WHERE nome_exercicio = %s", (nome_exercicio,))
        resultado = cursor.fetchone()

        if resultado:
            id_ex = resultado[0]
            cursor.execute("""
                INSERT INTO fato_treino (data_treino, id_exercicio, carga_kg, repeticoes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (row['DATA'], id_ex, row['KG'], row['REP']))
        else:
            print(f"Aviso: Exercício '{nome_exercicio}' não encontrado no banco!")

    conn.commit()
    print("Sucesso! O banco de dados foi atualizado.")

finally:
    if 'conn' in locals() and conn:
        cursor.close()
        conn.close()