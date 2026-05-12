import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# =====================================
# LOAD MODEL DAN SCALER
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RNN_PATH = os.path.join(
    BASE_DIR,
    "models",
    "rnn_final.h5"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)

print("📂 Loading RNN dari:", RNN_PATH)

# Validasi file model
if not os.path.exists(RNN_PATH):
    raise FileNotFoundError(
        f"File model tidak ditemukan: {RNN_PATH}"
    )

# Load model
# compile=False penting agar tidak error
rnn_model = load_model(
    RNN_PATH,
    compile=False
)

print("✅ RNN model berhasil dimuat")

# Load scaler
scaler = None

if os.path.exists(SCALER_PATH):
    print("📂 Loading Scaler dari:", SCALER_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Scaler berhasil dimuat")
else:
    print("⚠️ Scaler tidak ditemukan, prediksi tanpa normalisasi")


# =====================================
# PREDICT MAGNITUDE RNN
# =====================================

def predict_magnitude(data):
    try:
        # Ambil input
        last_data = data.get("last_magnitudes")

        # Validasi input
        if last_data is None:
            return {
                "error": "Parameter 'last_magnitudes' tidak ditemukan."
            }

        if not isinstance(last_data, list):
            return {
                "error": "'last_magnitudes' harus berupa list."
            }

        if len(last_data) != 10:
            return {
                "error": "Harus mengirim tepat 10 data magnitudo terakhir."
            }

        # Konversi ke float
        values = [float(x) for x in last_data]

        # Bentuk array (10, 1)
        arr = np.array(values).reshape(-1, 1)

        # Scaling jika tersedia
        if scaler is not None:
            arr = scaler.transform(arr)

        # =====================================
        # SHAPE SESUAI MODEL TRAINING:
        # (samples, timesteps, features)
        # (1, 10, 1)
        # =====================================
        X = arr.reshape(1, 10, 1)

        # Prediksi
        pred = rnn_model.predict(
            X,
            verbose=0
        )

        pred_value = float(pred[0][0])

        # Inverse transform jika scaler tersedia
        if scaler is not None:
            pred_value = scaler.inverse_transform(
                np.array([[pred_value]])
            )[0][0]

        # Batasi hasil agar realistis
        pred_value = max(0.0, pred_value)
        pred_value = round(float(pred_value), 2)

        return {
            "predicted_magnitude": pred_value,
            "input_sequence": values
        }

    except Exception as e:
        return {
            "error": str(e)
        }