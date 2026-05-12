import os
import numpy as np
import pandas as pd
import joblib

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


# =====================================
# KONFIGURASI PATH
# =====================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "gempa_2019_2024_bersih.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "rnn_final.h5")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
HISTORY_PATH = os.path.join(MODEL_DIR, "rnn_history.csv")


# =====================================
# 1. LOAD DATASET
# =====================================
print("📂 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Pastikan kolom Magnitude tersedia
df = df.dropna(subset=["Magnitude"])
magnitudes = df["Magnitude"].values.astype(float)

print(f"✅ Total data: {len(magnitudes)}")


# =====================================
# 2. NORMALISASI
# =====================================
print("🔄 Normalisasi data...")

scaler = MinMaxScaler()
scaled = scaler.fit_transform(
    magnitudes.reshape(-1, 1)
)


# =====================================
# 3. BUAT SEQUENCE
# =====================================
def create_sequence(data, step=10):
    X, y = [], []

    for i in range(len(data) - step):
        X.append(data[i:i + step])
        y.append(data[i + step])

    return np.array(X), np.array(y)


TIMESTEPS = 10

X, y = create_sequence(scaled, TIMESTEPS)

# Shape awal:
# X = (samples, 10, 1)
# y = (samples, 1)

X = X.reshape((X.shape[0], TIMESTEPS, 1))

print(f"✅ Shape X: {X.shape}")
print(f"✅ Shape y: {y.shape}")


# =====================================
# 4. SPLIT DATA
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=False
)

print(f"✅ Training samples: {len(X_train)}")
print(f"✅ Testing samples: {len(X_test)}")


# =====================================
# 5. BUILD MODEL
# =====================================
print("🧠 Building RNN model...")

model = Sequential([
    SimpleRNN(
        64,
        activation="tanh",
        input_shape=(TIMESTEPS, 1)
    ),
    Dense(32, activation="relu"),
    Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse"
)

model.summary()


# =====================================
# 6. CALLBACKS
# =====================================
early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)


# =====================================
# 7. TRAIN MODEL
# =====================================
print("🚀 Training model...")

history = model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping],
    verbose=1
)


# =====================================
# 8. SIMPAN MODEL
# =====================================
print("💾 Menyimpan model...")

model.save(MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print(f"✅ Model disimpan ke: {MODEL_PATH}")
print(f"✅ Scaler disimpan ke: {SCALER_PATH}")


# =====================================
# 9. SIMPAN HISTORY TRAINING
# =====================================
history_df = pd.DataFrame(history.history)
history_df.to_csv(HISTORY_PATH, index=False)

print(f"✅ History training disimpan ke: {HISTORY_PATH}")


# =====================================
# 10. HASIL AKHIR
# =====================================
print("\n=== TRAINING SELESAI ===")

if "loss" in history.history:
    print(f"Final Training Loss   : {history.history['loss'][-1]:.6f}")

if "val_loss" in history.history:
    print(f"Final Validation Loss : {history.history['val_loss'][-1]:.6f}")

print("🎉 RNN berhasil dilatih dan semua file tersimpan.")