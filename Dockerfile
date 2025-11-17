FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codice applicazione
COPY . .

# Crea directory per dati
RUN mkdir -p data output

# Esponi porta API
EXPOSE 8000

# Comando di avvio
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
