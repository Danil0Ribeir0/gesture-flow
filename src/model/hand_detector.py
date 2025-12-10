import cv2
import mediapipe as mp
import numpy as np
from model.interfaces import IGestureRecognizer
from utils.smoothing import LandmarkSmoother

class MediaPipeDetector(IGestureRecognizer):
    def __init__(self):

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = 1,
            model_complexity = 1,
            min_detection_confidence = 0.8,
            min_tracking_confidence = 0.8
        )

        self.smoother = LandmarkSmoother(alpha=0.6)

    def process_frame(self, frame: np.ndarray):
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(frame_rgb)

        frame.flags.writeable = True

        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                smoothed_data = self.smoother.process(raw_landmarks)

                for j, lm in enumerate(hand_landmarks.landmark):
                    lm.x = smoothed_data[j][0]
                    lm.y = smoothed_data[j][1]
                    lm.z = smoothed_data[j][2]

        return results

    def draw_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame