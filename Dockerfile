FROM python:3.11-slim

WORKDIR /app

COPY requirements_gestao_ativos.txt .
RUN pip install --no-cache-dir -r requirements_gestao_ativos.txt

COPY app_gestao_ativos_ia.py .
COPY .streamlit_config.toml .

CMD ["streamlit", "run", "app_gestao_ativos_ia.py"]
