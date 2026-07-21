import cv2

from hand_detector import HandDetector
from predictor import predict

camera = cv2.VideoCapture(0)

detector = HandDetector()

latest_prediction = {
    "gesture": "No Hand",
    "confidence": 0,
    "sentence": ""
}

# Sentence variables
sentence = []
last_prediction = ""


def generate_frames():

    global latest_prediction
    global sentence
    global last_prediction

    while True:

        success, frame = camera.read()

        if not success:
            break

        # Detect hand
        frame, features = detector.detect(frame)

        if len(features) == 63:

            gesture, confidence = predict(features)

            latest_prediction["gesture"] = gesture
            latest_prediction["confidence"] = confidence

            # Add only new gestures to the sentence
            if gesture != last_prediction:

                sentence.append(gesture)

                last_prediction = gesture

            latest_prediction["sentence"] = " ".join(sentence)

            # Show prediction on camera
            cv2.putText(
                frame,
                f"{gesture} ({confidence:.1f}%)",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        else:

            latest_prediction["gesture"] = "No Hand"
            latest_prediction["confidence"] = 0

            # Reset so the same gesture can be added again
            last_prediction = ""

        _, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )