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
# RUN SERVER
# =========================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)