from abc import ABC, abstractmethod
import numpy as np

class IGestureRecognizer(ABC):
    """
    Interface (Contrato) que define como qualquer reconhecedor de gestos deve se comportar.
    Se amanhã trocarmos o MediaPipe por outra IA, o resto do sistema não quebra.
    """
    @abstractmethod
    def process_frame(self, frame: np.ndarray):
        """
        Recebe um frame (imagem) e retorna o resultado do processamento.
        """
        pass