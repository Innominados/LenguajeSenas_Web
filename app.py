import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
from flask_cors import CORS
from mediapipe.python.solutions.holistic import Holistic
from tensorflow.keras.models import load_model
from gtts import gTTS
import pygame
from time import sleep, time
from werkzeug.utils import secure_filename
from metrics import extract_metrics
from funtions import mediapipe_detection, text_to_speech, get_actions, there_hand, format_sentences, draw_keypoints

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Rutas y constantes
ROOT_PATH = os.path.join(os.getcwd())
DATA_PATH = os.path.join(ROOT_PATH, "data")
MODELS_PATH = os.path.join(ROOT_PATH, "models")
MODEL_NAME = "modelfinal1.keras"

MAX_LENGTH_FRAMES = 15
MIN_LENGTH_FRAMES = 5
LENGTH_KEYPOINTS = 258  


# Cargar el modelo
model_path = os.path.join(MODELS_PATH, MODEL_NAME)
lstm_model = load_model(model_path)

# Funciones para procesamiento de imágenes

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33 * 4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21 * 3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21 * 3)
    keypoints = np.concatenate([pose, lh, rh])
    if keypoints.size != LENGTH_KEYPOINTS:
        keypoints = np.pad(keypoints, (0, LENGTH_KEYPOINTS - keypoints.size), mode='constant')
    return keypoints

def evaluate_model(model, threshold=0.7):
    count_frame = 0
    repe_sent = 1
    kp_sequence, sentence = [], []
    actions = get_actions(DATA_PATH)
    
    with Holistic() as holistic_model:
        video = cv2.VideoCapture(0)
        
        while video.isOpened():
            _, frame = video.read()

            image, results = mediapipe_detection(frame, holistic_model)
            kp_sequence.append(extract_keypoints(results))
            
            if len(kp_sequence) > MAX_LENGTH_FRAMES and there_hand(results):
                count_frame += 1
                
            else:
                if count_frame >= MIN_LENGTH_FRAMES:
                    res = model.predict(np.expand_dims(kp_sequence[-MAX_LENGTH_FRAMES:], axis=0))[0]

                    if res[np.argmax(res)] > threshold:
                        sent = actions[np.argmax(res)]
                        sentence.insert(0, sent)
                        text_to_speech(sent)
                        sentence, repe_sent = format_sentences(sent, sentence, repe_sent)
                        
                    count_frame = 0
                    kp_sequence = []

            cv2.rectangle(image, (0, 0), (640, 35), (245, 117, 16), -1)
            cv2.putText(image, ' | '.join(sentence), (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
            
            draw_keypoints(image, results)
            cv2.imshow('GestureGuide', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
                    
        video.release()
        cv2.destroyAllWindows()

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
    metrics_seq = []
    previous_results = None
    previous_time = None
    with Holistic() as holistic_model:
        for frame in frames:
            _, results = mediapipe_detection(frame, holistic_model)
            keypoints = extract_keypoints(results)
            kp_sequence.append(keypoints)
            current_time = time()
            delta_time = current_time - previous_time if previous_time else 1/15  # assuming 30 FPS if previous_time is None
            metrics = extract_metrics(results, previous_results, delta_time)

            # Convertir el diccionario de métricas a un array de NumPy
            metrics_array = np.concatenate([np.array(v).flatten() if isinstance(v, (list, np.ndarray)) else np.array([v]) for v in metrics.values()])
            metrics_seq.append(metrics_array)
            
            previous_results = results
            previous_time = current_time
            if len(kp_sequence) > MAX_LENGTH_FRAMES:
                kp_sequence.pop(0)
                metrics_seq.pop(0)

    if len(kp_sequence) == MAX_LENGTH_FRAMES:
        kp_sequence = np.array(kp_sequence)
        metrics_seq = np.array(metrics_seq)
        kp_sequence = np.expand_dims(kp_sequence, axis=0)
        metrics_seq = np.expand_dims(metrics_seq, axis=0)
        
        print(f"kp_sequence shape: {kp_sequence.shape}, dtype: {kp_sequence.dtype}")
        print(f"metrics_seq shape: {metrics_seq.shape}, dtype: {metrics_seq.dtype}")
        
        res = lstm_model.predict([kp_sequence, metrics_seq])[0]
        actions = get_actions(DATA_PATH)

        if res[np.argmax(res)] > 0.7:
            sent = actions[np.argmax(res)]
            text_to_speech(sent)
            return jsonify({'prediction': sent})
    
    return jsonify({'error': 'No valid prediction'}), 400

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
