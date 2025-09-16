# src/etl_aggregate.py
import pandas as pd
import os
import sqlite3

def run(db_path="viage_plus.db", out_dir="data/"):
    # conecta no SQLite usado pelo FastAPI
    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query("SELECT * FROM viagem_searches", conn, parse_dates=["data", "intencao_viagem_data"])
    conn.close()

    df["dias_para_viagem"] = (df["intencao_viagem_data"] - df["data"]).dt.days
    df["chave_repetida"] = df["user_id"].astype(str) + "|" + df["origem"] + "|" + df["destino"]
    df["pesquisa_repetida"] = df.groupby("chave_repetida")["data"].transform("count")

    os.makedirs(out_dir, exist_ok=True)

    # top rotas
    df.groupby(["origem", "destino"]).size().reset_index(name="pesquisas") \
        .to_csv(os.path.join(out_dir, "dashboard_top_rotas.csv"), index=False)

    # pesquisas diárias
    df.groupby(df["data"].dt.date).size().reset_index(name="pesquisas") \
        .to_csv(os.path.join(out_dir, "dashboard_pesquisas_diarias.csv"), index=False)

    # perfil de usuários
    df.groupby("user_id").agg(
        total_pesquisas=("user_id","count"),
        media_dias_para_viagem=("dias_para_viagem","mean"),
        num_alertas=("alerta","sum")
    ).reset_index() \
     .to_csv(os.path.join(out_dir, "dashboard_user_perfil.csv"), index=False)

    print(f"ETL concluído. Arquivos prontos em {out_dir}")

if __name__ == "__main__":
    run()
