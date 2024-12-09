

from dataclasses import dataclass



class PlanetConfig:

    def __init__(self, raw_config: dict):
        
        if "mass" not in raw_config:
            raise ValueError("Planets mass needs to be specified in config.yaml file.")
        if "radius" not in raw_config:
            raise ValueError("Planets radius needs to be specified in config file.")

        self.mass = float(raw_config['mass'])
        self.radius = float(raw_config['radius'])
        self.atmospheric_model = raw_config['atmosphere']['atmospheric_density_model']

        if self.atmospheric_model == "exponential_decay":
            try:
                self.sea_level_density = raw_config['atmosphere']['sea_level_density']
                self.scale_height = raw_config['atmosphere']['scale_height']
                
            except KeyError as e:
                raise ValueError("For this model, you need to specify the sea level air density \
                                 & scale of the model.")

    def validate(self):

        if self.mass <= 0:
            raise ValueError("Planets mass cannot be negative or zero.")
        if self.radius <= 0:
            raise ValueError("Planets radius cannot be negative or zero.")

        if type(self.atmospheric_model) != str:
            raise ValueError("Please enter a valid model and in the form of a string.")
        

