import joblib
import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def get_model_evaluation():

    # =========================
    # LOAD DATASET
    # =========================
    data_path = os.path.join(
        "data",
        "gempa_2019_2024_bersih.csv"
    )

    df = pd.read_csv(data_path)

    # =========================
    # FEATURE ENGINEERING
    # =========================
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df["hour"] = df["Datetime"].dt.hour
    df["dayofweek"] = df["Datetime"].dt.dayofweek
    df["month"] = df["Datetime"].dt.month
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)

    if "Distance_to_Fault" not in df.columns:
        df["Distance_to_Fault"] = 0

    # =========================
    # TARGET
    # =========================
    df["target"] = (df["Magnitude"] >= 5.5).astype(int)

    y = df["target"]

    # =========================
    # LOAD MODEL
    # =========================
    model_path = os.path.join(
        "backend",
        "models",
        "rf_final.pkl"
    )

    model = joblib.load(model_path)

    # =========================
    # AMBIL NAMA FITUR ASLI MODEL
    # =========================
    feature_columns = list(model.feature_names_in_)

    # Pastikan semua kolom tersedia
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Gunakan urutan kolom persis seperti model
    X = df[feature_columns]

    # =========================
    # SPLIT DATA
    # =========================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # =========================
    # PREDIKSI
    # =========================
    y_pred = model.predict(X_test)

    # =========================
    # CONFUSION MATRIX
    # =========================
    cm = confusion_matrix(y_test, y_pred)

    # =========================
    # METRICS
    # =========================
    result = {
        "confusion_matrix": cm.tolist(),
        "accuracy": round(
            accuracy_score(y_test, y_pred), 4
        ),
        "precision": round(
            precision_score(
                y_test,
                y_pred,
                zero_division=0
            ),
            4
        ),
        "recall": round(
            recall_score(
                y_test,
                y_pred,
                zero_division=0
            ),
            4
        ),
        "f1_score": round(
            f1_score(
                y_test,
                y_pred,
                zero_division=0
            ),
            4
        )
    }

    return result