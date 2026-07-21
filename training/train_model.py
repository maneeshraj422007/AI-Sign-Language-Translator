import os
import joblib
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ==========================
# Load Dataset
# ==========================

DATASET_PATH = "../datasets/csv/landmarks.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset Shape:", df.shape)
print(df["gesture"].value_counts())

# ==========================
# Features & Labels
# ==========================

X = df.drop("gesture", axis=1).values

y = df["gesture"].values

# ==========================
# Encode Labels
# ==========================

encoder = LabelEncoder()

y = encoder.fit_transform(y)

# Save encoder
os.makedirs("../models", exist_ok=True)
joblib.dump(encoder, "../models/label_encoder.pkl")

# ==========================
# Train/Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==========================
# Neural Network
# ==========================

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(63,)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(len(encoder.classes_), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ==========================
# Train
# ==========================

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=50,
    batch_size=16,
    verbose=1
)

# ==========================
# Evaluate
# ==========================

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

# ==========================
# Save Model
# ==========================

model.save("../models/sign_language_model.keras")

print("\n✅ Model saved to models/sign_language_model.keras")
print("✅ Label encoder saved to models/label_encoder.pkl")