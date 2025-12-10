from utils.gesture_enums import HandGesture
import time

class TextEngine:
    def __init__(self):
        self.current_sentence = ""
        
        self.last_gesture = None
        self.frame_count = 0
        self.confirm_threshold = 10
        
        self.last_added_time = 0
        self.cooldown_seconds = 2.0 

    def process_gesture(self, gesture: HandGesture):
        # Ignora gestos desconhecidos ou sem mão
        if gesture == HandGesture.UNKNOWN:
            self.frame_count = 0
            self.last_gesture = None
            return

        # Se o gesto é o mesmo do frame anterior, incrementa o contador
        if gesture == self.last_gesture:
            self.frame_count += 1
        else:
            # Se mudou, reseta a contagem (começa a validar o novo gesto)
            self.last_gesture = gesture
            self.frame_count = 0

        # Lógica de Confirmação
        if self.frame_count == self.confirm_threshold:
            self._add_word(gesture)

    def _add_word(self, gesture: HandGesture):
        current_time = time.time()
        
        # Verifica se já passou o tempo de cooldown (para não escrever "Paz Paz" muito rápido)
        if (current_time - self.last_added_time) < self.cooldown_seconds:
            return

        word_map = {
            HandGesture.VICTORY: "Paz",
            HandGesture.THUMBS_UP: "Curti",
            HandGesture.OPEN_HAND: "Ola",
            HandGesture.CLOSED_FIST: " ",
            HandGesture.POINTER: "Isso"
        }

        word = word_map.get(gesture, "")
        
        if word:
            # Lógica simples: Adiciona espaço se já tiver texto
            if self.current_sentence:
                self.current_sentence += " "
            
            self.current_sentence += word
            self.last_added_time = current_time
            print(f"Palavra adicionada: {word}") # Log para debug

    def get_sentence(self):
        return self.current_sentence
    
    def clear(self):
        self.current_sentence = ""