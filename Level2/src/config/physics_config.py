
from dataclasses import dataclass



@dataclass
class PhysicsConfig:

    def __init__(self, raw_config:dict):
        
        
        if "include_drag" not in raw_config:
            raise ValueError("You must give a boolean with the include_drag in config file.")
        if "include_lift" not in raw_config:
            raise ValueError("You must give a boolean with the include_lift in config file.")
        if "include_heating" not in raw_config:
            raise ValueError("You must give a boolean with the include_heating in config file.")
        if "include_heating" not in raw_config:
            raise ValueError("You must give a boolean with the include_heating in config file.")
        if "include_coriolis" not in raw_config:
            raise ValueError("You must give a boolean with the include_coriolis in config file.")
        
        self.include_drag = raw_config['include_drag']
        self.include_lift = raw_config['include_lift']
        self.include_heating = raw_config['include_heating']
        self.include_coriolis = raw_config['include_coriolis']


    def validate(self):
        if (type(self.include_drag) or type(self.include_lift) or type(self.include_heating) 
            or type(self.include_coriolis))  != bool:
            
            raise ValueError("The include_* statements can only be a boolean.")



