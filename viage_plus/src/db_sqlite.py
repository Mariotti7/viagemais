from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_PATH = os.path.join("data", "viage_plus.db")

# Cria engine
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

# Cria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()

# Modelo da tabela
class ViagemSearch(Base):
    __tablename__ = "viagem_searches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    data = Column(Date)                        # data da busca
    cidade_origem = Column(String)
    destino = Column(String)
    intencao_viagem_data = Column(Date)        # data pretendida da viagem
    preco = Column(Float)
    alerta = Column(Integer)                   # 0/1
    dias_para_viagem = Column(Integer)         # diferença em dias
    pesquisa_repetida = Column(Integer)        # 0/1 ou contador

# Criar as tabelas
def create_tables():
    Base.metadata.create_all(bind=engine)
