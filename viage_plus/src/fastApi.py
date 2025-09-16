from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Table, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///viage_plus.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
metadata = MetaData()

import sqlite3

def init_db():
    conn = sqlite3.connect("viage_plus.db")
    cursor = conn.cursor()
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
        dias_para_viagem INTEGER,
        pesquisa_repetida INTEGER
    )
    """)
    conn.commit()
    conn.close()

# Chame logo no início do seu FastAPI
init_db()


viagem_searches = Table(
    "viagem_searches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column("data", DateTime, nullable=False),
    Column("cidade_origem", String, nullable=False),
    Column("destino", String, nullable=False),
    Column("intencao_viagem_data", DateTime, nullable=False),
    Column("preco", Float, nullable=False),
    Column("alerta", Integer, default=0),
    Column("dias_para_viagem", Integer),
    Column("pesquisa_repetida", Integer, default=0),
)

def create_tables():
    metadata.create_all(engine)

app = FastAPI(title="Viage+ API")
create_tables()

class SearchEvent(BaseModel):
    user_id: int
    data: datetime
    cidade_origem: str
    destino: str
    intencao_viagem_data: datetime
    preco: float
    alerta: int = 0

@app.post("/events/search")
def receive_search(event: SearchEvent):
    try:
        dias_para_viagem = (event.intencao_viagem_data - event.data).days
        ins = viagem_searches.insert().values(
            user_id=event.user_id,
            data=event.data,
            cidade_origem=event.cidade_origem,
            destino=event.destino,
            intencao_viagem_data=event.intencao_viagem_data,
            preco=event.preco,
            alerta=event.alerta,
            dias_para_viagem=dias_para_viagem,
            pesquisa_repetida=0
        )
        with engine.connect() as conn:
            conn.execute(ins)
        return {"status": "ok", "message": "Busca registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "running"}
