from flask import Flask, Response, jsonify
from flask_cors import CORS

from camera import generate_frames, latest_prediction

app = Flask(__name__)

# Enable CORS so the frontend can access the backend
CORS(app)


@app.route("/")
def home():
    return {
        "message": "AI Sign Language Translator Backend Running",
        "status": "success"
    }


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/prediction")
def prediction():
    return jsonify({
        "gesture": latest_prediction["gesture"],
        "confidence": latest_prediction["confidence"],
        "sentence": latest_prediction["sentence"]
    })


@app.route("/clear")
def clear_sentence():
    from camera import sentence, latest_prediction

    sentence.clear()

    latest_prediction["sentence"] = ""

    return jsonify({
        "message": "Sentence cleared"
    })


if __name__ == "__main__":
    app.run(debug=True)