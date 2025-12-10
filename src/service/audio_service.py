import pyttsx3
import threading

class AudioService:
    def __init__(self):
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "brazil" in voice.id.lower() or "portuguese" in voice.id.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 180)
    
    def speak(self, text: str):
        if not text:
            return
        
        t = threading.Thread(target=self._speak_thread, args=(text,))
        t.daemon = True
        t.start()

    def _speak_thread(self, text: str):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Erro no TTS: {e}")