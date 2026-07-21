import cv2
import csv
import os
import mediapipe as mp

GESTURE = "Thank you"          # Change this for each gesture
SAMPLES = 200              # Number of samples to collect

SAVE_DIR = "../datasets/csv"
CSV_FILE = os.path.join(SAVE_DIR, "landmarks.csv")

os.makedirs(SAVE_DIR, exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

drawer = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

count = 0

# Create CSV header if file doesn't exist
if not os.path.exists(CSV_FILE):
    header = ["gesture"]
    for i in range(21):
        header.extend([f"x{i}", f"y{i}", f"z{i}"])

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

print("Press 's' to save a sample.")
print("Press 'q' to quit.")

while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    row = None

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        drawer.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        row = [GESTURE]

        for lm in hand.landmark:
            row.extend([lm.x, lm.y, lm.z])

    cv2.putText(
        frame,
        f"Gesture: {GESTURE}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Samples: {count}/{SAMPLES}",
        (10, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.imshow("Dataset Collector", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s") and row is not None:

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        count += 1

        print(f"Saved sample {count}")

        if count >= SAMPLES:
            print("Collection complete!")
            break

    elif key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()