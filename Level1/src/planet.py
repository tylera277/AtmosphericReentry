
import numpy as np

from .config.planet_config import PlanetConfig


class Planet:
    def __init__(self, config: PlanetConfig):
        
        self.mass = config.mass
        self.radius = config.radius
    

    def calculate_gravity(self, position_of_object: np.ndarray) -> np.ndarray:

        # the gravitational constant
        G = 6.67430e-11

        dist = np.linalg.norm(position_of_object)

        if dist == 0:
            raise ZeroDivisionError("Position vector cannot be zero.")
        
        return -G * self.mass * position_of_object / (dist**3)

