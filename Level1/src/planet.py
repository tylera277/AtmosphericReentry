
import numpy as np

from .config.planet_config import PlanetConfig


class Planet:
    """
    All parameters pertaining to the planet that youre wanting to use.
    Written so that any planet conditions and characteristics can be used.
    """
    def __init__(self, config: PlanetConfig):
        
        self.mass = config.mass
        self.radius = config.radius
    

    def calculate_gravity(self, position_of_object: np.ndarray) -> np.ndarray:
        """
        Calculates, given the position of the spacecraft, the gravitational force
        it would feel from this planet.
        Its assuming that the planet is at the origin of the coordinate frame that
        is being used.
        """


        # the gravitational constant
        G = 6.67430e-11

        dist = np.linalg.norm(position_of_object)

        if dist == 0:
            raise ZeroDivisionError("Position vector cannot be zero.")
        
        return -G * self.mass * position_of_object / (dist**3)

