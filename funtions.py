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

def mediapipe_detection(image, model):
    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.flip(image, 1)
    return image, results

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

def get_actions(path):
    out = []
    for action in os.listdir(path):
        name, ext = os.path.splitext(action)
        if ext == ".h5":
            out.append(name)
    return out

def there_hand(results):
    return results.left_hand_landmarks or results.right_hand_landmarks

def format_sentences(sent, sentence, repe_sent):
    if len(sentence) > 1 and sent == sentence[1]:
        repe_sent += 1
    else:
        repe_sent = 1
    if repe_sent > 2:
        sentence = sentence[:1]
    return sentence, repe_sent

def draw_keypoints(image, results):
    if results.pose_landmarks:
        for landmark in results.pose_landmarks.landmark:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    if results.left_hand_landmarks:
        for landmark in results.left_hand_landmarks.landmark:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    if results.right_hand_landmarks:
        for landmark in results.right_hand_landmarks.landmark:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)