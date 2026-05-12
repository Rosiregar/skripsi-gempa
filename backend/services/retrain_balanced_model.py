import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


def retrain_balanced_model():
    """
    Melatih ulang Random Forest dengan class_weight='balanced'
    untuk menangani data yang tidak seimbang.
    """

    # =====================================
    # LOAD DATASET
    # =====================================
    data_path = os.path.join(
        "data",
        "gempa_2019_2024_bersih.csv"
    )

    df = pd.read_csv(data_path)

    # =====================================
    # FEATURE ENGINEERING
    # =====================================
    df["Datetime"] = pd.to_datetime(df["Datetime"])

    df["hour"] = df["Datetime"].dt.hour
    df["dayofweek"] = df["Datetime"].dt.dayofweek
    df["month"] = df["Datetime"].dt.month
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(int)

    # Jika kolom belum tersedia
    if "Distance_to_Fault" not in df.columns:
        df["Distance_to_Fault"] = 0

    # =====================================
    # TARGET
    # Risiko tinggi jika Magnitude >= 5.5
    # =====================================
    df["target"] = (df["Magnitude"] >= 5.5).astype(int)

    # =====================================
    # FITUR
    # NOTE:
    # Magnitude TIDAK digunakan untuk menghindari data leakage
    # =====================================
    feature_columns = [
        "Depth",
        "Latitude",
        "Longitude",
        "Distance_to_Fault",
        "hour",
        "dayofweek",
        "month",
        "is_weekend"
    ]

    # Pastikan semua fitur tersedia
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    # Hapus missing value
    df = df.dropna(subset=feature_columns + ["target"])

    X = df[feature_columns]
    y = df["target"]

    # =====================================
    # INFORMASI DISTRIBUSI KELAS
    # =====================================
    print("\n=== DISTRIBUSI TARGET ===")
    print(y.value_counts())

    # =====================================
    # SPLIT DATA
    # =====================================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # =====================================
    # TRAIN MODEL BALANCED
    # =====================================
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # =====================================
    # PREDIKSI
    # =====================================
    y_pred = model.predict(X_test)

    # =====================================
    # METRICS
    # =====================================
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )
    cm = confusion_matrix(y_test, y_pred)

    result = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "confusion_matrix": cm.tolist(),
        "feature_columns": feature_columns
    }

    # =====================================
    # SIMPAN MODEL
    # =====================================
    model_dir = os.path.join("backend", "models")
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(
        model_dir,
        "rf_balanced.pkl"
    )

    joblib.dump(model, model_path)

    print(f"\n✅ Model berhasil disimpan ke: {model_path}")

    return result


if __name__ == "__main__":

    result = retrain_balanced_model()

    print("\n=== HASIL MODEL BALANCED ===")
    print(f"Accuracy  : {result['accuracy']:.4f}")
    print(f"Precision : {result['precision']:.4f}")
    print(f"Recall    : {result['recall']:.4f}")
    print(f"F1 Score  : {result['f1_score']:.4f}")

    print("\nConfusion Matrix:")
    print(result["confusion_matrix"])

    print("\nFeature Columns:")
    for col in result["feature_columns"]:
        print(f"- {col}")