# src/predict_next_purchase.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

def prepare_features(df):
    # df must contain: user_id, dias_para_viajem, alerta, pesquisa_repetida, price_ceiling
    X = df[["dias_para_viajem", "alerta", "pesquisa_repetida", "preco"]].fillna(0)
    return X

def derive_label(df, purchase_window_days=14):
    # For the mock dataset we don't have purchases; we will simulate label:
    # If alerta==1 and dias_para_viajem <= purchase_window_days and pesquisa_repetida>=1 -> label 1 (likely buy)
    return ((df["alerta"]==1) & (df["dias_para_viajem"] <= purchase_window_days) & (df["pesquisa_repetida"]>=1)).astype(int)

def run(csv_path="data/viage_mais_pesquisas.csv", model_out="models/next_purchase_rf.pkl"):
    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    df = pd.read_csv(csv_path, parse_dates=["data", "intencao_viagem_data"])
    df["dias_para_viajem"] = (df["intencao_viagem_data"] - df["data"]).dt.days
    df["chave_repetida"] = df["user_id"].astype(str) + "|" + df["cidade_origem"] + "|" + df["destino"]
    df["pesquisa_repetida"] = df.groupby("chave_repetida")["data"].transform("count")
    df["label"] = derive_label(df)
    X = prepare_features(df)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    joblib.dump(clf, model_out)
    print(f"Model saved to {model_out}")

if __name__ == "__main__":
    run()
