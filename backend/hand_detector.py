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

        # This will store x,y,z values for all 21 landmarks
        feature_vector = []

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                # Draw hand skeleton
                self.drawer.draw_landmarks(
                    frame,
                    hand,
                    self.mpHands.HAND_CONNECTIONS
                )

                h, w, _ = frame.shape

                for idx, lm in enumerate(hand.landmark):

                    # -----------------------------
                    # Save normalized coordinates
                    # -----------------------------
                    feature_vector.extend([
                        lm.x,
                        lm.y,
                        lm.z
                    ])

                    # -----------------------------
                    # Convert to pixels only for drawing
                    # -----------------------------
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                    cv2.putText(
                        frame,
                        str(idx),
                        (cx + 5, cy - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        (255, 255, 255),
                        1
                    )

        return frame, feature_vector