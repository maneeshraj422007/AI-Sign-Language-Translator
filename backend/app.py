from flask import Flask, Response
from camera import generate_frames

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Sign Language Translator Backend Running"


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)