import cv2
import numpy as np
import mediapipe as mp
from view.interfaces import IView

class OpenCV_View(IView):
    def __init__(self, window_name="Gesture Flow"):
        self.window_name = window_name
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def render(self, frame: np.ndarray, gesture_name: str, landmarks_results):
        frame = cv2.flip(frame, 1)

        if gesture_name and gesture_name != "Desconhecido":
            cv2.rectangle(frame, (10, 10), (350, 60), (0, 0, 0), -1)
            cv2.putText(frame, f"Gesto: {gesture_name}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow(self.window_name, frame)
    
    def should_close(self) -> bool:
        return cv2.waitKey(5) & 0xFF == ord('q')

    def close(self):
        cv2.destroyAllWindows()