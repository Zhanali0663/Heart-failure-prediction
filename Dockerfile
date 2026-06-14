FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт Streamlit (Hugging Face требует порт 7860)
EXPOSE 7860

# Запускаем FastAPI в фоне + Streamlit на порту 7860
CMD uvicorn api.fastapi:app --host 0.0.0.0 --port 8000 & \
    streamlit run ui/app.py --server.port 7860 --server.address 0.0.0.0
