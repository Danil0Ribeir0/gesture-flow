# src/main.py
import cv2
import time
from model.hand_detector import MediaPipeDetector
from model.gesture_classifier import GestureClassifier

def main():
    # Instancia Models
    detector = MediaPipeDetector()
    classifier = GestureClassifier()
    
    cap = cv2.VideoCapture(0)
    
    print("Iniciando Gesture Flow...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # 1. Detectar Mão
        results = detector.process_frame(frame)
        
        gesture_name = ""

        # 2. Se achou mão, classificar gesto
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extrai a lista de landmarks
                landmarks_list = hand_landmarks.landmark
                
                # Classifica
                gesture_enum = classifier.process(landmarks_list)
                gesture_name = gesture_enum.value

                # Desenha o esqueleto
                detector.draw_landmarks(frame, results)

        # 3. Desenhar interface (Texto na tela)
        # Espelha o frame (flip) para ficar natural
        frame = cv2.flip(frame, 1)
        
        # Escreve o texto do gesto (Atenção: como demos flip, desenhamos depois)
        if gesture_name:
            cv2.rectangle(frame, (10, 10), (300, 60), (0, 0, 0), -1) # Fundo preto pro texto
            cv2.putText(frame, gesture_name, (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Gesture Flow - Fase 3', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()