import os
import joblib
import numpy as np
from datetime import datetime



try:
    model = joblib.load(MODEL_PATH)
    print("Model berhasil dimuat! ✅")
except Exception as e:
    model = None
    print(f"Gagal memuat model karena: {e} ❌")
# =========================
# LOAD MODEL (sekali saja)
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_final.pkl")

print("📂 Loading model dari:", MODEL_PATH)

model = joblib.load(MODEL_PATH)


# =========================
# FUNCTION PREDIKSI
# =========================
def predict_risk(data=None):
    try:
        # waktu sekarang
        now = datetime.now()

        hour = now.hour
        month = now.month
        dayofweek = now.weekday()
        is_weekend = 1 if dayofweek >= 5 else 0

        # sementara dummy (nanti kita upgrade pakai geo distance)
        distance_to_fault = 0.5

        # input ke model
        X = np.array([[hour, month, dayofweek, is_weekend, distance_to_fault]])

        pred = model.predict(X)[0]

        if hasattr(model, "predict_proba"):
            prob = float(np.max(model.predict_proba(X)))
        else:
            prob = 0.0

        return {
            "prediction": int(pred),
            "probability": prob,
            "features_used": {
                "hour": hour,
                "month": month,
                "dayofweek": dayofweek,
                "is_weekend": is_weekend,
                "distance_to_fault": distance_to_fault
            }
        }

    except Exception as e:
        return {"error": str(e)}
