

import numpy as np

from .config.spacecraft_config import SpacecraftConfig


class Spacecraft:
    def __init__(self, config: SpacecraftConfig):
        
        self.position = np.array(config.position, dtype=float)
        self.velocity = np.array(config.velocity, dtype=float)
        
        self.mass = config.mass
        self.drag_coefficient = config.drag_coeff
        self.cross_sect_area = config.cross_sect_area
        

        