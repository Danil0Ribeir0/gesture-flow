from utils.gesture_enums import HandGesture
import time

class TextEngine:
    def __init__(self):
        self.current_sentence = ""
        self.last_gesture = None
        self.frame_count = 0
        self.confirm_threshold = 10
        self.last_added_time = 0
        self.cooldown_seconds = 1.0

    def process_gesture(self, gesture: HandGesture):
        if gesture == HandGesture.UNKNOWN:
            self.frame_count = 0
            self.last_gesture = None
            return None

        if gesture == self.last_gesture:
            self.frame_count += 1
        else:
            self.last_gesture = gesture
            self.frame_count = 0

        if self.frame_count == self.confirm_threshold:
            return self._add_word(gesture)
        
        return None

    def _add_word(self, gesture: HandGesture):
        current_time = time.time()
        
        if (current_time - self.last_added_time) < self.cooldown_seconds:
            return None

        word_map = {
            HandGesture.VICTORY: "Paz",
            HandGesture.THUMBS_UP: "Curti",
            HandGesture.OPEN_HAND: "Ola",
            HandGesture.CLOSED_FIST: "Apagar",
            HandGesture.POINTER: "Isso"
        }

        word = word_map.get(gesture, "")
        
        if word:
            if word == "Apagar":
                self.current_sentence = ""
                self.last_added_time = current_time
                return "Texto apagado"
            
            if self.current_sentence:
                self.current_sentence += " "
            
            self.current_sentence += word
            self.last_added_time = current_time
            return word
            
        return None

    def get_sentence(self):
        return self.current_sentence
    
    def clear(self):
        self.current_sentence = ""