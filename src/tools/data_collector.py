import cv2
import mediapipe as mp
import numpy as np
import copy
import csv
import os

FILE_NAME = 'libras_dataset.csv'
CLASSES = ['A', 'B', 'C', 'D', 'E']

class DataCollector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.setup_csv()
    
    def setup_csv(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, mode='w', newline='') as f:
                writer = csv.writer(f)
                header = ['label']
                for i in range(21):
                    header.append(f'x{i}')
                    header.append(f'y{i}')
                writer.writerow(header)
    
    def normalize_landmarks(self, landmarks):
        temp_landmark_list = copy.deepcopy(landmarks)

        base_x, base_y = 0, 0
        normalized_list = []

        for index, landmark in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark.x, landmark.y

            normalized_list.append(landmark.x - base_x)
            normalized_list.append(landmark.y - base_y)

        max_value = max(list(map(abs, normalized_list)))

        def normalize_(n):
            return n / max_value

        final_list = list(map(normalize_, normalized_list))

    def save_data(self, label, landmarks):
        try:
            data = self.normalize_landmarks(landmarks)

            data.insert(0, label)

            with open(FILE_NAME, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            print(f"Amostra salva para classe '{label}'")
        except Exception as e:
            print(f"Erro ao salvar: {e}")

    def run(self):
        print("--- COLETOR DE DADOS LIBRAS ---")
        print(f"Pressione as teclas correspondentes para salvar: {CLASSES}")
        print("Pressione 'Q' para sair.")

        import copy

        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success: continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    key = cv2.waitKey(1) & 0xFF
                    
                    # Verifica se a tecla apertada é uma das nossas classes (ex: 'a', 'b')
                    for cls in CLASSES:
                        if key == ord(cls.lower()):
                            self.save_data(cls, hand_landmarks.landmark)

            cv2.imshow("Data Collector", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    DataCollector().run()