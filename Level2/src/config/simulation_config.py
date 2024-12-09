
from dataclasses import dataclass


@dataclass
class SimulationConfig:

    def __init__(self, raw_config: dict):

        if "start_time" not in raw_config:
            raise ValueError("Simulation start time must be specified in config file.")
        if "end_time" not in raw_config:
            raise ValueError("Simulation end time must be specified in config file.")
        if "time_step_size" not in raw_config:
            raise ValueError("Simulation time step size must be specified in config file.")
        
        self.start_time = raw_config['start_time']
        self.end_time = raw_config["end_time"]
        self.time_step_size = raw_config['time_step_size']
    
    
    def validate(self):

        if self.start_time < 0:
            raise ValueError("Please just use a non-negative start time.")
        if self.end_time < self.start_time:
            raise ValueError("End time must be equal to or greater than start time.")
        if self.time_step_size == 0:
            raise ValueError("Time step size must be a nonzero number.")
        
