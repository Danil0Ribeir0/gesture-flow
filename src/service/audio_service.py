# src/services/audio_service.py
import pyttsx3
import threading

class AudioService:
    def __init__(self):
        # Apenas descobrimos o ID da voz portuguesa na inicialização
        # Não guardamos a 'engine' aqui para evitar conflito de threads
        self.voice_id = self._find_portuguese_voice_id()
    
    def _find_portuguese_voice_id(self):
        """
        Cria uma engine temporária apenas para achar o ID da voz BR.
        """
        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        selected_id = None
        
        for voice in voices:
            # Tenta achar voz PT-BR
            if "brazil" in voice.id.lower() or "portuguese" in voice.id.lower():
                selected_id = voice.id
                break
        
        # Opcional: Se não achar, pega a primeira (inglês)
        if selected_id is None and len(voices) > 0:
            selected_id = voices[0].id
            
        # Destrói a engine temporária para liberar recursos
        del temp_engine
        return selected_id

    def speak(self, text: str):
        """
        Dispara a thread de fala.
        """
        if not text:
            return

        # Passamos o ID da voz para a thread usar
        t = threading.Thread(target=self._speak_thread, args=(text, self.voice_id))
        t.daemon = True
        t.start()

    def _speak_thread(self, text: str, voice_id):
        """
        Esta função roda em paralelo. 
        Ela cria sua PRÓPRIA engine, fala e morre.
        Isso evita o erro de 'COM Object' do Windows.
        """
        try:
            # 1. Inicializa uma nova engine exclusiva para esta thread
            engine = pyttsx3.init()
            
            # 2. Configura a voz (se tivermos achado uma)
            if voice_id:
                engine.setProperty('voice', voice_id)
            
            engine.setProperty('rate', 180) # Velocidade
            
            # 3. Fala
            engine.say(text)
            engine.runAndWait()
            
            # A engine morre aqui automaticamente ao fim da função
        except Exception as e:
            print(f"Erro na thread de áudio: {e}")