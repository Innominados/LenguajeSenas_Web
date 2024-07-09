import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from mediapipe.python.solutions.holistic import Holistic
from tensorflow.keras.models import load_model # type: ignore
from gtts import gTTS
import pygame
from time import sleep
from typing import NamedTuple
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Rutas y constantes
ROOT_PATH = os.path.join(os.getcwd())
DATA_PATH = os.path.join(ROOT_PATH, "data")
MODELS_PATH = os.path.join(ROOT_PATH, "models")
MODEL_NAME = "modeloprueba4.keras"
MAX_LENGTH_FRAMES = 15
MIN_LENGTH_FRAMES = 5

# Cargar el modelo
model_path = os.path.join(MODELS_PATH, MODEL_NAME)
lstm_model = load_model(model_path)

# Funciones para procesamiento de imágenes
def mediapipe_detection(image, model):
    # Reflejar horizontalmente la imagen
    image = cv2.flip(image, 1)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Reflejar nuevamente la imagen para que esté en la orientación original
    image = cv2.flip(image, 1)
    
    return image, results



def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = "speech.mp3"
    tts.save(filename)
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)

    pygame.mixer.quit()
    pygame.quit()

    os.remove(filename)

# API Endpoint para predecir
@app.route('/predict', methods=['POST'])
def predict():
    if 'video' not in request.files:
        return jsonify({'error': 'No video provided'}), 400

    file = request.files['video']
    filename = secure_filename(file.filename)
    file_path = os.path.join(ROOT_PATH, filename)
    file.save(file_path)

    cap = cv2.VideoCapture(file_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    os.remove(file_path)

    if not frames:
        return jsonify({'error': 'No frames captured from video'}), 400

    kp_sequence = []
    with Holistic() as holistic_model:
        for frame in frames:
            _, results = mediapipe_detection(frame, holistic_model)
            keypoints = extract_keypoints(results)
            kp_sequence.append(keypoints)
            if len(kp_sequence) > MAX_LENGTH_FRAMES:
                kp_sequence.pop(0)

    if len(kp_sequence) == MAX_LENGTH_FRAMES:
        res = lstm_model.predict(np.expand_dims(kp_sequence, axis=0))[0]
        actions = get_actions(DATA_PATH)

        if res[np.argmax(res)] > 0.7:
            sent = actions[np.argmax(res)]
            text_to_speech(sent)
            return jsonify({'prediction': sent})
    
    return jsonify({'error': 'No valid prediction'}), 400

def get_actions(path):
    out = []
    for action in os.listdir(path):
        name, ext = os.path.splitext(action)
        if ext == ".txt":
            out.append(name)
    return out

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/starter')
def starter_page():
    return render_template('starter-page.html')

@app.route('/service-details')
def service_details():
    return render_template('service-details.html')

@app.route('/tutorial-page')
def tutorial_page():
    return render_template('tutorial-page.html')

if __name__ == '__main__':
    app.run(debug=True)
