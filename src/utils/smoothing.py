import numpy as np

class LandmarkSmoother:
    def __init__(self, alpha = 0.6):
        self.alpha = alpha
        self.previous_landmarks = None

    def process(self, current_landmarks_list):
        current_array = np.array(current_landmarks_list)

        if self.previous_landmarks is None:
            self.previous_landmarks = current_array
            return current_array
        
        smoothed_array = (self.alpha * current_array) + ((1 - self.alpha) * self.previous_landmarks)

        self.previous_landmarks = smoothed_array

        return smoothed_array