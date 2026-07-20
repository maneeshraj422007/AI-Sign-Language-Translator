import cv2
from hand_detector import HandDetector

camera = cv2.VideoCapture(0)

detector = HandDetector()


def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame = detector.detect(frame)

        _, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame +
            b'\r\n'
        )