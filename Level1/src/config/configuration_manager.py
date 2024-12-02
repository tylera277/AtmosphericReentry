

from .spacecraft_config import SpacecraftConfig
from .planet_config import PlanetConfig
from .simulation_config import SimulationConfig

from pathlib import Path

import yaml



class ConfigurationManager:
    """
    Class which handles all of the configuration for each base component of the program.
    Allowing the main program to only need to call this once and the initial 
    configuration is complete.
    """
    
    def __init__(self, config_path: Path):

        self.raw_config_file = self._load_yaml_file(config_path)

        self.spacecraft = SpacecraftConfig(self.raw_config_file['spacecraft']['initial_state'])
        self.planet = PlanetConfig(self.raw_config_file['planet'])
        self.simulation = SimulationConfig(self.raw_config_file['simulation'])


        self.validate_all()


    def _load_yaml_file(self, path: Path) -> dict:
        """
        Opens the config.yaml file which has the user defined parameters for the simulation.
        """
        try:
            with open(path) as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
             raise ValueError(f"Error parsing configuration file: {e}")
        

    def validate_all(self):
        """
        Runs all of the separate validations for each component as a check to make sure
        the parameters arent grossly incorrect before theyre sent into the simulation.
        """
        self.spacecraft.validate()
        self.planet.validate()
        self.simulation.validate()

