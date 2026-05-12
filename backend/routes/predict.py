from flask import Blueprint, request, jsonify

from services.model_service import predict_risk
from services.evaluation_service import get_model_evaluation
from services.rnn_service import predict_magnitude as predict_rnn_magnitude

from database.db import db
from database.models import PredictionHistory

import joblib
import pandas as pd
import os

# =====================================
# BLUEPRINT
# =====================================

predict_bp = Blueprint("predict", __name__)

# =====================================
# LOAD MODEL MAGNITUDE
# =====================================

MODEL_PATH = os.path.join(
    "backend",
    "models",
    "magnitude_model.pkl"
)

magnitude_model = None

if os.path.exists(MODEL_PATH):
    magnitude_model = joblib.load(MODEL_PATH)
    print("✅ magnitude_model.pkl berhasil dimuat")
else:
    print("⚠️ magnitude_model.pkl tidak ditemukan")


# =====================================
# PREDICT RISIKO GEMPA
# =====================================

@predict_bp.route("/predict", methods=["POST"])
def predict():

    data = request.json

    # Prediksi risiko
    result = predict_risk(data)
    
    # Debug hasil prediksi
    print("=" * 50)
    print("INPUT DATA:", data)
    print("HASIL PREDIKSI:", result)
    print("Prediction:", result.get("prediction"))
    print("Probability:", result.get("probability"))
    print("=" * 50)

    # Ambil input
    magnitudo = data.get("magnitudo")
    depth = data.get("depth")
    lat = data.get("lat")
    lon = data.get("lon")

    # Hasil model
    prediction = result.get("prediction")
    probability = result.get("probability")

    # Simpan ke history
    history = PredictionHistory(
        magnitudo=magnitudo,
        depth=depth,
        lat=lat,
        lon=lon,
        prediction=prediction,
        probability=probability
    )

    db.session.add(history)
    db.session.commit()

    return jsonify(result)


# =====================================
# HISTORY PREDIKSI
# =====================================

@predict_bp.route("/history", methods=["GET"])
def history():

    histories = PredictionHistory.query.order_by(
        PredictionHistory.created_at.desc()
    ).all()

    results = []

    for h in histories:
        results.append({
            "magnitudo": h.magnitudo,
            "depth": h.depth,
            "lat": h.lat,
            "lon": h.lon,
            "prediction": h.prediction,
            "probability": h.probability,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(results)


# =====================================
# PREDICT MAGNITUDE
# =====================================

@predict_bp.route("/predict-magnitude", methods=["POST"])
def predict_magnitude():

    # Cek model
    if magnitude_model is None:
        return jsonify({
            "error": "Model magnitude tidak ditemukan."
        }), 500

    try:
        # Ambil request JSON
        data = request.json

        if not data:
            return jsonify({
                "error": "Request body kosong."
            }), 400

        depth = data.get("depth")
        lat = data.get("lat")
        lon = data.get("lon")

        # Validasi input
        if depth is None or lat is None or lon is None:
            return jsonify({
                "error": "depth, lat, dan lon wajib diisi."
            }), 400

        # Konversi ke float
        depth = float(depth)
        lat = float(lat)
        lon = float(lon)

        # DataFrame input
        input_data = pd.DataFrame([{
            "Depth": depth,
            "Latitude": lat,
            "Longitude": lon
        }])

        # Prediksi magnitude
        prediction = magnitude_model.predict(input_data)[0]

        # Response
        return jsonify({
            "depth": depth,
            "lat": lat,
            "lon": lon,
            "predicted_magnitude": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# =====================================
# MODEL EVALUATION
# =====================================

@predict_bp.route("/evaluation", methods=["GET"])
def evaluation():

    try:
        result = get_model_evaluation()
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# =====================================
# PREDICT MAGNITUDE RNN
# =====================================

@predict_bp.route("/predict-rnn", methods=["POST"])
def predict_rnn():

    try:
        data = request.json

        if not data:
            return jsonify({
                "error": "Request body kosong."
            }), 400

        sequence = data.get("sequence")

        if not sequence or len(sequence) != 10:
            return jsonify({
                "error": "Sequence harus berisi 10 nilai magnitudo."
            }), 400

        # Format sesuai rnn_service.py
        payload = {
            "last_magnitudes": sequence
        }

        result = predict_rnn_magnitude(payload)

        if "error" in result:
            return jsonify(result), 400

        return jsonify({
            "predicted_magnitude": round(
                float(result["predicted_magnitude"]),
                2
            )
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500