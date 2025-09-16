import pandas as pd
import sqlite3

DB_PATH = "data/viage_plus.db"

def run_query(query, description):
    print(f"\n--- {description} ---")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df.head(10))
    return df


if __name__ == "__main__":
    # 1. Top trechos por busca
    run_query("""
        SELECT cidade_origem, destino, COUNT(*) AS searches
        FROM viagem_searches
        GROUP BY cidade_origem, destino
        ORDER BY searches DESC
        LIMIT 10;
    """, "Top trechos")

    # 2. Origens mais frequentes
    run_query("""
        SELECT cidade_origem, COUNT(*) AS qtd_searches
        FROM viagem_searches
        GROUP BY cidade_origem
        ORDER BY qtd_searches DESC
        LIMIT 10;
    """, "Origens mais buscadas")

    # 3. Intenção (alerta e pesquisa_repetida)
    run_query("""
        SELECT
          SUM(CASE WHEN alerta=1 THEN 1 ELSE 0 END) AS total_alerts,
          SUM(CASE WHEN pesquisa_repetida > 1 THEN 1 ELSE 0 END) AS total_pesquisa_repetida
        FROM viagem_searches;
    """, "Sinais de intenção")

    # 4. Janela provável de compra
    run_query("""
        SELECT user_id, cidade_origem, destino, dias_para_viagem, alerta, pesquisa_repetida
        FROM viagem_searches
        WHERE alerta=1 AND dias_para_viagem <= 14
        LIMIT 10;
    """, "Clientes com alta probabilidade de compra")