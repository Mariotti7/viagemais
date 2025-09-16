import sqlite3
import pandas as pd
import random
import datetime
import os

DB_PATH = "data/viage_plus.db"

# Garante que a pasta exista
os.makedirs("data", exist_ok=True)

# Conectar ao banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS viagem_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    data TEXT,
    cidade_origem TEXT,
    destino TEXT,
    intencao_viagem_data TEXT,
    preco REAL,
    alerta INTEGER,
    pesquisa_repetida INTEGER,
    dias_para_viagem INTEGER
);
""")
conn.commit()

# Gerar dados fictícios
cidade_origem = ["São Paulo", "Campinas", "Rio de Janeiro", "Belo Horizonte"]
destino = ["Curitiba", "Florianópolis", "Porto Alegre", "Salvador"]

rows = []
for i in range(200):
    user_id = random.randint(1000, 1020)
    data = datetime.datetime.now() - datetime.timedelta(days=random.randint(0,30))
    cidade_origem = random.choice(cidade_origem)
    destino = random.choice(destino)
    intencao_viagem_data = data + datetime.timedelta(days=random.randint(5,30))
    preco = random.choice([100,150,200,250,300])
    alerta = random.choice([0,1])
    pesquisa_repetida = random.randint(1,3)
    dias_para_viagem = (intencao_viagem_data - data).days
    
    rows.append((user_id, data.isoformat(), cidade_origem, destino,
                 intencao_viagem_data.isoformat(), preco,
                 alerta, pesquisa_repetida, dias_para_viagem))

df = pd.DataFrame(rows, columns=[
    "user_id","data","cidade_origem","destino",
    "intencao_viagem_data","preco","alerta",
    "pesquisa_repetida","dias_para_viagem"
])

df.to_sql("viagem_searches", conn, if_exists="append", index=False)

print("Banco populado!")
conn.close()
