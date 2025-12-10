import cv2
from model.hand_detector import MediaPipeDetector
from model.gesture_classifier import GestureClassifier
from model.text_engine import TextEngine
from view.opencv_view import OpenCV_View
from service.audio_service import AudioService

class MainController:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.detector = MediaPipeDetector()
        self.classifier = GestureClassifier()
        self.text_engine = TextEngine()
        self.view = OpenCV_View(window_name="Gesture Flow v2.0")
        self.audio_service = AudioService()
        self.audio_service.speak("Sistema iniciado")

    def run(self):
        while self.camera.isOpened():
            success, frame = self.camera.read()
            if not success:
                continue

            results = self.detector.process_frame(frame)
            current_gesture_name = "..."
            
            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0].landmark
                
                gesture_enum = self.classifier.process(landmarks)
                current_gesture_name = gesture_enum.value
                
                word_confirmed = self.text_engine.process_gesture(gesture_enum)
                
                if word_confirmed:
                    self.audio_service.speak(word_confirmed)

            final_sentence = self.text_engine.get_sentence()
            self.view.render(frame, current_gesture_name, final_sentence, results)

            if self.view.should_close():
                break

        self._cleanup()

    def _cleanup(self):
        self.audio_service.speak("Encerrando sistema")
        self.camera.release()
        self.view.close()