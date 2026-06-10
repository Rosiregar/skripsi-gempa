import os
from flask import Flask
from routes.predict import predict_bp
from routes.rnn import rnn_bp
from database.db import db

app = Flask(__name__)

# =========================
# DATABASE CONFIG
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gempa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Inisialisasi database di tingkat global (di luar __main__)
# Ini wajib agar Gunicorn di Cloud Run bisa membuat file database saat aplikasi start
with app.app_context():
    db.create_all()

# =========================
# REGISTER BLUEPRINT
# =========================
app.register_blueprint(predict_bp, url_prefix="/api")
app.register_blueprint(rnn_bp, url_prefix="/api")

# =========================
# ROUTE UTAMA
# =========================
@app.route("/")
def home():
    return {
        "message": "API Prediksi Gempa Aktif 🚀"
    }

# =========================
# RUN SERVER (LOKAL)
# =========================
# Blok ini hanya berjalan jika Anda mengetik 'python app.py' di lokal.
# Di Cloud Run, blok ini akan diabaikan karena gunicorn langsung memanggil objek 'app'.
if __name__ == "__main__":
    # Menggunakan port dinamis dari environment variable GCP (default ke 5000 jika lokal)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
