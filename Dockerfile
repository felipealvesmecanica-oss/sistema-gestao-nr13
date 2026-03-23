dockerfileFROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_gestao_ativos_ia.py .
COPY .streamlit .streamlit

EXPOSE 10000

CMD ["streamlit", "run", "app_gestao_ativos_ia.py", "--server.port=10000", "--server.address=0.0.0.0
