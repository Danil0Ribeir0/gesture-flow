# src/controllers/main_controller.py
import cv2
from model.hand_detector import MediaPipeDetector
from model.gesture_classifier import GestureClassifier
from view.opencv_view import OpenCV_View

class MainController:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.detector = MediaPipeDetector()
        self.classifier = GestureClassifier()
        self.view = OpenCV_View(window_name="Gesture Flow v1.0")

    def run(self):
        print("Iniciando Controller...")
        
        while self.camera.isOpened():
            success, frame = self.camera.read()
            if not success:
                print("Erro ao ler câmera.")
                continue

            results = self.detector.process_frame(frame)
            
            gesture_name = ""
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0].landmark
                
                gesture_enum = self.classifier.process(landmarks)
                gesture_name = gesture_enum.value
         
                self.detector.draw_landmarks(frame, results)

            self.view.render(frame, gesture_name, results)

            if self.view.should_close():
                break

        self._cleanup()

    def _cleanup(self):
        """Libera recursos ao fechar"""
        self.camera.release()
        self.view.close()
        print("Sistema encerrado.")