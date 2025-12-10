import cv2
import numpy as np
import mediapipe as mp
from view.interfaces import IView

class OpenCV_View(IView):
    def __init__(self, window_name="Gesture Flow"):
        self.window_name = window_name
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def render(self, frame: np.ndarray, current_gesture: str, sentence: str, landmarks_results):
        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, (0, 0), (640, 40), (50, 50, 50), -1)
        cv2.putText(frame, f"Detectando: {current_gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 400), (640, 480), (0, 0, 0), -1)
        alpha = 0.6
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        cv2.putText(frame, sentence, (20, 450), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow(self.window_name, frame)
    
    def should_close(self) -> bool:
        return cv2.waitKey(5) & 0xFF == ord('q')

    def close(self):
        cv2.destroyAllWindows()