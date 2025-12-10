# src/main.py
import cv2
from model.hand_detector import MediaPipeDetector

def main():
    # 1. Instancia nosso Detector (Model)
    detector = MediaPipeDetector()
    
    # 2. Abre a Webcam (0 geralmente é a câmera padrão)
    cap = cv2.VideoCapture(0)
    
    print("Iniciando Gesture Flow... Pressione 'q' para sair.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignorando frame vazio da câmera.")
            continue

        # 3. Usa nossa classe para processar a IA
        results = detector.process_frame(frame)
        
        # 4. Desenha o esqueleto (só para visualizarmos se funcionou)
        frame = detector.draw_landmarks(frame, results)

        # Espelha a imagem para ficar mais natural (como um espelho)
        cv2.imshow('Gesture Flow - Teste de Model', cv2.flip(frame, 1))

        # Sai se apertar 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()