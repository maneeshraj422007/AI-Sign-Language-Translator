import os
import joblib
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "sign_language_model.keras")
ENCODER_PATH = os.path.join(BASE_DIR, "..", "models", "label_encoder.pkl")

model = tf.keras.models.load_model(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


def predict(features):

    if len(features) != 63:
        return "No Hand", 0

    X = np.array(features).reshape(1, 63)

    prediction = model.predict(X, verbose=0)

    confidence = float(np.max(prediction)) * 100

    class_index = np.argmax(prediction)

    gesture = encoder.inverse_transform([class_index])[0]

    return gesture, round(confidence, 2)