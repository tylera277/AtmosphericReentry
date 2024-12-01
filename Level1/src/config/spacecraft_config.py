

from dataclasses import dataclass




@dataclass
class SpacecraftConfig:

    def __init__(self, raw_config: dict):
        
        
        
        # Check to make sure the needed values are indeed found
        if "position" not in raw_config:
            raise ValueError("Spacecraft position must be specified in config.yaml file.")
        if "velocity" not in raw_config:
            raise ValueError("Spacecraft velocity must be specified in config.yaml file.")


        # Assign the initial values pulled to variables
        self.position = raw_config['position']
        self.velocity = raw_config['velocity']

        # Check the values that were pulled to make sure they make sense and wont
        # brake anything in the code.
        #self.validate()


    def validate(self):

        if len(self.position) != 3:
            raise ValueError("Position must be a 3D vector.")
        if len(self.velocity) != 3:
            raise ValueError("Velocity must be a 3D vector.")
        
        if self.position == [0, 0, 0]:
            raise ValueError("Position vector cannot be set to be the origin.")