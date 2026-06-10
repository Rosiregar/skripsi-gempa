FROM python:3.11-slim

WORKDIR /app

COPY . .

# Menginstal dependency aplikasi
RUN pip install --no-cache-dir -r requirements.txt

# Menjalankan Flask menggunakan gunicorn memakai file app.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
