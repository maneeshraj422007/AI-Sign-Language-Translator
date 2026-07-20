import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6
        )

        self.drawer = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            self.drawer.draw_landmarks(
                frame,
                hand,
                self.mpHands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            for idx, lm in enumerate(hand.landmark):

                x = int(lm.x * w)
                y = int(lm.y * h)

                landmarks.append([idx, x, y])

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(
                    frame,
                    str(idx),
                    (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2
                )
        return frame, landmarks