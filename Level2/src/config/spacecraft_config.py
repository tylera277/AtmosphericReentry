

from dataclasses import dataclass


@dataclass
class SpacecraftConfig:

    def __init__(self, raw_config: dict):
        
        
        
        # Check to make sure the needed values are indeed found
        if "position" not in raw_config['initial_state']:
            raise ValueError("Spacecraft position must be specified in config.yaml file.")
        if "velocity" not in raw_config['initial_state']:
            raise ValueError("Spacecraft velocity must be specified in config.yaml file.")

        if "drag_coefficient" not in raw_config['design_parameters']:
            raise ValueError("Spacecraft needs to have drag coefficient for ")

        # Assign the initial values pulled to variables
        self.position = raw_config['initial_state']['position']
        self.velocity = raw_config['initial_state']['velocity']

        # Design parameters 
        self.drag_coeff = raw_config['design_parameters']['drag_coefficient']
        self.cross_sect_area = raw_config['design_parameters']['cross_sectional_area']
        self.mass = raw_config['design_parameters']['mass']

    def validate(self):
        """
        Check the values that were pulled to make sure they make sense and wont
        immediately brake anything in the code.
        """
        if len(self.position) != 3:
            raise ValueError("Position must be a 3D vector.")
        if len(self.velocity) != 3:
            raise ValueError("Velocity must be a 3D vector.")
        
        if self.position == [0, 0, 0]:
            raise ValueError("Position vector cannot be set to be the origin.")
        if self.mass <= 0:
            raise ValueError("Mass of spacecraft needs to be greater than zero.")
        if self.drag_coeff <= 0:
            raise ValueError("The mass of the spacecraft must be greater than zero.")
        if self.cross_sect_area <= 0:
            raise ValueError("Cross sectional area of spacecraft must be greater than zero.")
        

        