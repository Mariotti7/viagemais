INSTRUÇÕES DE EXECUÇÃO (local)

1) Crie virtualenv e instale dependências:
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt

2) Gerar dados mock:
   python src/generate_mock_data.py
   --> gera data/viagem_mais_pesquisas.csv

3) Rodar ETL / gerar CSVs para dashboard:
   python src/etl_aggregate.py
   --> gera data/dashboard_top_routes.csv, dashboard_daily_searches.csv, dashboard_user_profiles.csv

   Conecte esses CSVs no Looker Studio (via Google Sheets: importe o CSV para Google Sheets ou use upload direto)

4) Criar DB local (SQLite) e inserir CSV via SQLAlchemy or COPY:
   - Para testes, crie DB sqlite padrão através do db.py metadata create_tables (feito automaticamente ao rodar fastapi_app)
   - Para Postgres, ajuste VIAGE_DB_URL na variável de ambiente (ex: export VIAGE_DB_URL="postgresql://user:pass@host/db")

5) Rodar API local (opcional, para registrar eventos de busca):
   uvicorn src.fastapi_app:app --reload --port 8000

   POST example:
   curl -X POST "http://localhost:8000/events/search" -H "Content-Type: application/json" \
        -d '{"user_id":1001,"search_date":"2025-08-01T10:00:00","origin":"São Paulo","destination":"Campinas","intended_trip_date":"2025-08-10T00:00:00","price_ceiling":120,"alert_set":1}'

6) Treinar modelo de previsão (opcional):
   python src/predict_next_purchase.py
   --> cria models/next_purchase_rf.pkl

7) Exportar relatórios para Looker Studio:
   - Faça upload dos CSVs gerados por etl_aggregate.py para Google Sheets (ou BigQuery) e conecte no Looker Studio.
   - Monte os gráficos: Top Routes, Daily Searches, User Profiles, KPI de probabilidade de compra (use outputs do modelo ou heurísticas)

8) Como rodar o App(front_app):
   - No terminal execute o comando: streamlit run src/front_app.py

9) Abrir o looker:
   - https://lookerstudio.google.com/reporting/b5088e83-5fa5-4652-8552-78305580b1b9

10) Link do PITCH:
   - https://youtu.be/tfpIQtzI4HU
