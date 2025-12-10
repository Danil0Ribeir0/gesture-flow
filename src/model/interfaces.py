from abc import ABC, abstractmethod
import numpy as np

class IGestureRecognizer(ABC):
    @abstractmethod
    def process_frame(self, frame: np.ndarray):
        """
        Recebe um frame (imagem) e retorna o resultado do processamento.
        """
        pass