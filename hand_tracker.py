import cv2
import math
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading hand landmarker model...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Done.")

class HandTracker:
    def __init__(self):
        download_model()
        base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7,
            running_mode=vision.RunningMode.IMAGE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def get_landmarks(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.detector.detect(mp_image)
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

    def get_index_thumb(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        index = landmarks[8]
        thumb = landmarks[4]
        ix, iy = int(index.x * w), int(index.y * h)
        tx, ty = int(thumb.x * w), int(thumb.y * h)
        distance = math.hypot(ix - tx, iy - ty)
        angle = math.degrees(math.atan2(iy - ty, ix - tx))
        return (ix, iy), (tx, ty), distance, angle

    def get_hand_center(self, landmarks, frame_shape):
        h, w = frame_shape[:2]
        wrist = landmarks[0]
        return int(wrist.x * w), int(wrist.y * h)

    def draw_landmarks(self, frame, landmarks):
        pass
