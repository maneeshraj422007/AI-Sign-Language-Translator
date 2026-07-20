from flask import Flask, Response, jsonify
from flask_cors import CORS

from camera import generate_frames, latest_prediction

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return "AI Sign Language Translator Backend Running"


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/prediction")
def prediction():
    return jsonify(latest_prediction)


if __name__ == "__main__":
    app.run(debug=True)