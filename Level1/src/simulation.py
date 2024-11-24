
import numpy as np

from .spacecraft import Spacecraft
from .planet import Planet


class Simulation:
    def __init__(self, config: dict, spacecraft: Spacecraft, planet: Planet):
        

        self.spacecraft = spacecraft
        self.planet = planet

        try:
            self.dt = float(config['time_step_size'])
            self.start_time = float(config['start_time'])
            self.end_time = float(config['end_time'])
        except KeyError as e:
            print(f"Missing configuration parameter: {e}")



    def run(self):
        time = self.start_time

        # Lists to store the positions of the craft over time
        position = []
        velocity = []


        # Main simulation loop
        while time < self.end_time:
    
            k_r, k_v = self.rungeKutta4()
            
            # Im not using index 0 as I think that may add confusion for me during
            # the implementations steps, me having to remember to always subtract one.
            print(self.spacecraft.position)
            print(k_r[1])
            print('-----------')
            self.spacecraft.position += (self.dt / 6.0) * (k_r[1] + 2*k_r[2] + 2*k_r[3] + k_r[4])
            self.spacecraft.velocity += (self.dt / 6.0) * (k_v[1] + 2*k_v[2] + 2*k_v[3] + k_v[4])
            
            # this 10 represents the writing frequency.
            # Im hardcoding its value for right now in order to experiment.
            if time % (10*self.dt):
                position.append(self.spacecraft.position)
                velocity.append(self.spacecraft.velocity)
        

            time += self.dt
            
        return position
    
    def rungeKutta4(self):
        # Arrays storing the k terms
        k_r = np.zeros((5, 3))
        k_v = np.zeros((5, 3))


        k_v[1] = self.planet.calculate_gravity(self.spacecraft.position)
        k_r[1] = self.spacecraft.velocity

        k_v[2] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt / 2.0)*k_r[1] )
        k_r[2] = self.spacecraft.velocity * k_v[1] * (self.dt / 2.0)

        k_v[3] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt / 2.0)*k_r[2] )
        k_r[3] = self.spacecraft.velocity * k_v[2] * (self.dt / 2.0)

        k_v[3] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt)*k_r[3] )
        k_r[3] = self.spacecraft.velocity * k_v[3] * self.dt

        return k_r, k_v

