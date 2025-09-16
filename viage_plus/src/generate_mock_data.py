# src/generate_mock_data.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate(path="data/viage_mais_pesquisas.csv", n_users=500, n_events=2500):
    np.random.seed(42)
    cities = ["São Paulo", "Campinas", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Porto Alegre", "Florianópolis"]
    routes = [(o, d) for o in cities for d in cities if o != d]

    start_date = datetime.now() - timedelta(days=60)
    dates = [start_date + timedelta(days=np.random.randint(0, 60)) for _ in range(n_events)]
    intended_dates = [d + timedelta(days=np.random.randint(1, 40)) for d in dates]
    user_ids = np.random.randint(1000, 1000 + n_users, size=n_events)
    chosen_routes = [routes[np.random.randint(0, len(routes))] for _ in range(n_events)]
    price_max = np.random.randint(60, 300, size=n_events)
    alerts = np.random.choice([0,1], size=n_events, p=[0.7, 0.3])  # alert set indicates stronger intent

    df = pd.DataFrame({
        "user_id": user_ids,
        "data": dates,
        "cidade_origem": [r[0] for r in chosen_routes],
        "destino": [r[1] for r in chosen_routes],
        "intencao_viagem_data": intended_dates,
        "preco": price_max,
        "alerta": alerts
    })

    df["dias_para_viajem"] = (pd.to_datetime(df["intencao_viagem_data"]).dt.date.astype("datetime64[ns]") - pd.to_datetime(df["data"]).dt.date.astype("datetime64[ns]")).dt.days
    df["pesquisa_repetida_chave"] = df["user_id"].astype(str) + "|" + df["cidade_origem"] + "|" + df["destino"]
    repeat_counts = df.groupby("pesquisa_repetida_chave")["data"].transform("count")
    df["pesquisa_repetida"] = (repeat_counts > 1).astype(int)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Mock data saved to {path}")

if __name__ == "__main__":
    generate()
