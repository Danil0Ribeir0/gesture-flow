from abc import ABC, abstractmethod
import numpy as np

class IView(ABC):
    @abstractmethod
    def render(self, frame: np.ndarray, gesture_name: str, landmarks_results):
        """
        Recebe os dados processados e mostra ao usuário.
        """
        pass
    @abstractmethod
    def should_close(self) -> bool:
        """
        Verifica se o usuário pediu para sair.
        """
        pass