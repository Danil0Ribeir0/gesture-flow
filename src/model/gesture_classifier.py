import mediapipe as mp
from utils.gesture_enums import HandGesture

class GestureClassifier:
    def __init__(self):
        self.tip_ids = [4, 8, 12, 16, 20]

    def process(self, landmarks) -> HandGesture:
        if not landmarks:
            return HandGesture.UNKNOWN

        fingers_up = []

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]

        is_lateral_open = abs(thumb_tip.x - thumb_mcp.x) > 0.05 
        
        is_vertical_open = thumb_tip.y < thumb_ip.y

        if is_lateral_open or is_vertical_open:
            fingers_up.append(1)
        else:
            fingers_up.append(0)

        for id in range(1, 5):
            tip_y = landmarks[self.tip_ids[id]].y
            pip_y = landmarks[self.tip_ids[id] - 2].y
            
            if tip_y < pip_y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        return self._decide_gesture(fingers_up)

    def _decide_gesture(self, fingers_up) -> HandGesture:
        # Todos levantados
        if fingers_up == [1, 1, 1, 1, 1]:
            return HandGesture.OPEN_HAND
            
        # Nenhum levantado (ou só o dedão fechado dependendo da angulação)
        if fingers_up == [0, 0, 0, 0, 0] or fingers_up == [1, 0, 0, 0, 0]: 
            return HandGesture.CLOSED_FIST
            
        # Indicador e Médio levantados (Vitória)
        if fingers_up == [0, 1, 1, 0, 0]:
            return HandGesture.VICTORY
            
        # Só o dedão (Like) - *Pode precisar de ajuste dependendo da mão*
        if fingers_up[0] == 1 and fingers_up[1] == 0 and fingers_up[2] == 0 and fingers_up[3] == 0:
             return HandGesture.THUMBS_UP
             
        # Só o indicador
        if fingers_up == [0, 1, 0, 0, 0] or fingers_up == [1, 1, 0, 0, 0]:
            return HandGesture.POINTER

        return HandGesture.UNKNOWN