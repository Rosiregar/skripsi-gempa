from flask import Blueprint, request, jsonify
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# =========================
# LOAD MODEL
# =========================
rnn_model = load_model("backend/models/rnn_final.h5", compile=False)
scaler = joblib.load("backend/models/rf_final.pkl")

# =========================
# BLUEPRINT
# =========================
rnn_bp = Blueprint("rnn", __name__)

# =========================
# ROUTE PREDIKSI RNN
# =========================
@rnn_bp.route("/predict-rnn", methods=["POST"])
def predict_rnn():

    try:
        data = request.json

        last_magnitudes = data["last_magnitudes"]

        # VALIDASI
        if len(last_magnitudes) != 5:
            return jsonify({
                "error": "Harus kirim 5 data magnitudo terakhir"
            }), 400

        # =========================
        # PREPROCESS
        # =========================
        arr = np.array(last_magnitudes).reshape(-1, 1)

        scaled = scaler.transform(arr)

        x_input = scaled.reshape(1, 5, 1)

        # =========================
        # PREDIKSI
        # =========================
        pred_scaled = rnn_model.predict(x_input)

        pred = scaler.inverse_transform(pred_scaled)

        hasil = float(pred[0][0])

        return jsonify({
            "predicted_magnitude": round(hasil, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500