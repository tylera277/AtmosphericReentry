

import numpy as np


class Spacecraft:
    def __init__(self, config: dict):
        """ Initialize spacecraft parameters from the config file. """
        try:
            self.position = np.array(config['initial_state']['position'], dtype=float)
            self.velocity = np.array(config['initial_state']['velocity'], dtype=float)
        except KeyError as e:
            print(f"Missing configuration parameter: {e}")

        