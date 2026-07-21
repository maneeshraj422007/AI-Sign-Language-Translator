from predictor import predict
import cv2
from hand_detector import HandDetector

camera = cv2.VideoCapture(0)

detector = HandDetector()

latest_prediction = {
    "gesture": "--",
    "confidence": 0
}


def generate_frames():

    global latest_prediction

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame, features = detector.detect(frame)

        # Temporary prediction
        if len(features) == 63:

            gesture, confidence = predict(features)

            latest_prediction["gesture"] = gesture
            latest_prediction["confidence"] = confidence

        else:

            latest_prediction["gesture"] = "No Hand"
            latest_prediction["confidence"] = 0

        _, buffer = cv2.imencode(".jpg", frame)

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + buffer.tobytes() +
            b'\r\n'
        )