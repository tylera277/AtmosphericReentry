
import numpy as np


class Planet:
    def __init__(self, config: dict):
        "Initialize parameters for the planet from configuration file."
        try:
            self.mass = float(config['mass'])
            self.radius = float(config['radius'])
        except KeyError as e:
            print(f"Missing configuration parameter: {e}")
    

    def calculate_gravity(self, position_of_object: np.ndarray) -> np.ndarray:

        # the gravitational constant
        G = 6.67430e-11

        dist = np.linalg.norm(position_of_object)
    
        if dist == 0:
            raise ZeroDivisionError("Position vector cannot be zero.")

        return -G * self.mass * position_of_object / (dist**3)

