FROM python:3.11-slim

WORKDIR /app

# Системные зависимости (нужны для некоторых пакетов)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Hugging Face требует порт 7860
EXPOSE 7860

# Запуск: FastAPI на 8000, Streamlit на 7860
CMD uvicorn api.fastapi:app --host 0.0.0.0 --port 8000 & \
    streamlit run ui/app.py --server.port 7860 --server.address 0.0.0.0
