from flask import Flask, request, jsonify
from flask_cors import CORS
#import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# =========================
# LOAD MODELS
# =========================
#model = tf.keras.models.load_model("disease_model.h5")
crop_model = pickle.load(open("crop_model.pkl", "rb"))

# =========================
# CLASS NAMES (FIXED)
# =========================
class_names = [
    "Tomato Early blight",
    "Tomato Late blight",
    "Tomato Target Spot",
    "Tomato Bacterial spot",
    "Tomato healthy",
    "Potato Early blight",
    "Potato Late blight",
    "Pepper bell healthy"
]

# =========================
# CURE SUGGESTIONS
# =========================
cures = {
    "Tomato Early blight": "Use fungicides like mancozeb.",
    "Tomato Late blight": "Apply copper-based fungicides.",
    "Tomato Target Spot": "Use chlorothalonil spray.",
    "Tomato Bacterial spot": "Use copper sprays and avoid overhead watering.",
    "Tomato healthy": "No disease detected. Maintain proper care.",
    "Potato Early blight": "Use fungicides and crop rotation.",
    "Potato Late blight": "Apply fungicides and remove infected plants.",
    "Pepper bell healthy": "Healthy plant. Keep monitoring."
}

# =========================
# IMAGE PREDICTION
# =========================
def predict_image(img_path):
    return "Tomato healthy"

# =========================
# HOME ROUTE (ADD THIS)
# =========================
@app.route("/")
def home():
    return "Backend is running 🚀"

# =========================
# DISEASE API
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["image"]

        os.makedirs("uploads", exist_ok=True)
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        result = predict_image(filepath)
        cure = cures.get(result, "No specific cure found")

        return jsonify({
            "disease": result,
            "cure": cure
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# CROP API
# =========================
@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json

        features = [
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])
        ]

        prediction = crop_model.predict([features])[0]

        return jsonify({"crop": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run()