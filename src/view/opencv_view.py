import cv2
import numpy as np
import mediapipe as mp
from view.interfaces import IView

class OpenCV_View(IView):
    def __init__(self, window_name="Gesture Flow"):
        self.window_name = window_name
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        self.drawing_styles = mp.solutions.drawing_styles
        self.connection_spec = self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        self.landmark_spec = self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)

    def render(self, frame: np.ndarray, current_gesture: str, sentence: str, landmarks_results):
        if landmarks_results and landmarks_results.multi_hand_landmarks:
            for hand_landmarks in landmarks_results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.landmark_spec,
                    self.connection_spec
                )

        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, (0, 0), (640, 40), (30, 30, 30), -1)
        
        color_status = (200, 200, 200)
        if current_gesture and current_gesture != "Desconhecido":
            color_status = (0, 255, 0)
            
        cv2.putText(frame, f"Detectando: {current_gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_status, 2)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 400), (640, 480), (0, 0, 0), -1)
        alpha = 0.7
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        cv2.putText(frame, sentence, (20, 450), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow(self.window_name, frame)

    def should_close(self) -> bool:
        return cv2.waitKey(5) & 0xFF == ord('q')

    def close(self):
        cv2.destroyAllWindows()