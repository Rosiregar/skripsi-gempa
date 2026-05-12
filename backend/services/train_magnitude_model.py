import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("data/gempa_2019_2024_bersih.csv")

# =========================
# FITUR INPUT
# =========================

X = df[[
    "Depth",
    "Latitude",
    "Longitude"
]]

# =========================
# TARGET
# =========================

y = df["Magnitude"]

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
# TRAIN MODEL
# =========================

model = RandomForestRegressor()

model.fit(X_train, y_train)

# =========================
# SAVE MODEL
# =========================

joblib.dump(
    model,
    "backend/models/magnitude_model.pkl"
)

print("Model magnitude berhasil disimpan!")