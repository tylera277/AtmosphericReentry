

from dataclasses import dataclass



class PlanetConfig:

    def __init__(self, raw_config: dict):
        
        if "mass" not in raw_config:
            raise ValueError("Planets mass needs to be specified in config.yaml file.")
        if "radius" not in raw_config:
            raise ValueError("Planets radius needs to be specified in config file.")

        self.mass = float(raw_config['mass'])
        self.radius = float(raw_config['radius'])

    def validate(self):

        if self.mass <= 0:
            raise ValueError("Planets mass cannot be negative or zero.")
        if self.radius <= 0:
            raise ValueError("Planets radius cannot be negative or zero.")

