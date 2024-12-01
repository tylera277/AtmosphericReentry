
import numpy as np

from .spacecraft import Spacecraft
from .planet import Planet


class Simulation:
    """
    A class that performs the numerical simulation of spacecraft dynamics around a planet.

    This simulation uses a 4th-order Runge-Kutta method to solve the equations of motion
    for a spacecraft under the gravitational influence of a planet.
    
    
    """

    def __init__(self, config: dict, spacecraft: Spacecraft, planet: Planet):
        """
        Initialize the simulation with configuration parameters and objects.

        Args:
            config (dict): configuration dictionary containing simulation parameters user specifies
                - "time_step_size": Time step for numerical integration.
                - "start_time": Initial simulation time.
                - "end_time": Final simulation time.
            spacecraft (Spacecraft): Spacecraft object with initial conditions.
            plaet (Planet): Planet object providing for planet characteristics such as gravity.

        Raises:
            KeyError: If required configuration parameters are missing from the config file.
        """

        self.spacecraft = spacecraft
        self.planet = planet


        try:
            self.dt = float(config['time_step_size'])
            self.start_time = float(config['start_time'])
            self.end_time = float(config['end_time'])
        except KeyError as e:
            print(f"Missing configuration parameter: {e}")


        # Initialize simulation history arrays
        self.time_elapsed = self.end_time  # Updated if the simulation terminates early
        self.position = []
        self.velocity = []


    def run(self):
        """
        Execute the simulation using a 4th order Runge-Kutta integrator.

        The simulation rungs from start_time to end_time unless terminated early
        due to impact of the planets surface. Position and velocity histories are stored
        for later analysis.

        Returns:
            None: Results are stored in self.position and self.velocity.

        
        """


        time = self.start_time        


        # Main simulation loop
        while time < self.end_time:
    
            k_r, k_v = self.rungeKutta4()
            
            # Update the spacecraft state using RK4 weighted averages
            self.spacecraft.position += ((self.dt / 6.0) * (k_r[1] + 2*k_r[2] + 2*k_r[3] + k_r[4]))
            self.spacecraft.velocity += ((self.dt / 6.0) * (k_v[1] + 2*k_v[2] + 2*k_v[3] + k_v[4]))
            
            # Store current state
            self.position.append((self.spacecraft.position).tolist())
            self.velocity.append((self.spacecraft.velocity).tolist())
        
            
            # Check for surface impact.
            if np.linalg.norm(self.spacecraft.position) <= self.planet.radius:
                print("Hit the surface! Ending simulation...")
                print(self.spacecraft.position)

                self.time_elapsed = time
                break
            

            time += self.dt
            

    
    def rungeKutta4(self):
        """
        Perform one step of the 4ht order Runge-Kutta integration.

        This method calculates the four stages of the RK4 method for both
        position and velocity updates. The k terms represent the slopes at
        different points within the time step.

        Returns:
            k_r & k_v (numpy ndarray): Two numpy arrays containing the RK4 terms for 
                position and velocity respectively. Each array has shape (5,3) where 
                index 0 is unused and indices 1-4 correspond to the four RK4 stages.
        
        """


        # Arrays storing the k terms
        k_r = np.zeros((5, 3))
        k_v = np.zeros((5, 3))

        # First stage
        k_v[1] = self.planet.calculate_gravity(self.spacecraft.position)
        k_r[1] = self.spacecraft.velocity

        # Second stage
        k_v[2] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt / 2.0)*k_r[1] )
        k_r[2] = self.spacecraft.velocity + k_v[1] * (self.dt / 2.0)

        # Third stage
        k_v[3] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt / 2.0)*k_r[2] )
        k_r[3] = self.spacecraft.velocity + k_v[2] * (self.dt / 2.0)

        # Fourth stage
        k_v[4] = self.planet.calculate_gravity( self.spacecraft.position + (self.dt)*k_r[3] )
        k_r[4] = self.spacecraft.velocity + k_v[3] * self.dt

        return k_r, k_v

