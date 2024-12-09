
import numpy as np

from dataclasses import dataclass
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod

from .config.simulation_config import SimulationConfig
from .spacecraft import Spacecraft
from .planet import Planet
from .physics import Physics

class Simulation:
    """
    A class that performs the numerical simulation of spacecraft dynamics around a planet.

    This simulation uses a 4th-order Runge-Kutta method to solve the equations of motion
    for a spacecraft under the gravitational influence of a planet.
    
    
    """

    def __init__(self, 
                 config: SimulationConfig, 
                 spacecraft: Spacecraft, 
                 planet: Planet,
                 physics: Physics) -> None:
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
        self.physics = physics
        self.config = config
        


        # Initialize simulation history arrays
        self.time_elapsed = self.config.end_time  # Updated if the simulation terminates early
        self._times: List[float] = []
        self._position: List[np.ndarray] = []
        self._velocity: List[np.ndarray] = []

        self._is_complete: bool = False
        self._termination_reason: str = "Not started."


    def run(self):# -> None:
        """
        Execute the simulation using a 4th order Runge-Kutta integrator.

        The simulation rungs from start_time to end_time unless terminated early
        due to impact of the planets surface. Position and velocity histories are stored
        for later analysis.

        Returns:
            None: Results are stored in self._position and self._velocity.

        
        """

        current_time = self.config.start_time      

        # Main simulation loop
        while current_time < self.config.end_time:
            print("curr time: ", current_time)
            # Advance one time step
            try:
                self._integrate_step()
            except ValueError as e:
                self._termination_reason = f"Integration error: {str(e)}"

            current_time += self.config.time_step_size
            self._store_state(current_time)

            # Check for termination conditions.
            # (i.e. it hit the planets surface)
            if self._check_surface_impact():
                print("Surface Impact")
                self._termination_reason = "Surface Impact"
                break

        self._termination_reason = "Simulation complete."


    def _integrate_step(self) -> None:
        """
        Gets the k terms and then updates the positions and velocities of the spacecraft
        """
        k_r, k_v = self._calculate_rungeKutta4_terms()

        # Update the spacecraft state using RK4 weighted averages
        self.spacecraft.position += ((self.config.time_step_size / 6.0) * (k_r[1] + 2*k_r[2] + 2*k_r[3] + k_r[4]))
        self.spacecraft.velocity += ((self.config.time_step_size / 6.0) * (k_v[1] + 2*k_v[2] + 2*k_v[3] + k_v[4]))

    
    def _calculate_rungeKutta4_terms(self) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        The math for calculating each of the interconnected components k terms,
        that are needed for the runge kutta implementation.

        The k terms represent the slopes at
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
        k_v[1] = self.physics.get_acceleration(self.spacecraft.position, self.spacecraft.velocity)
        k_r[1] = self.spacecraft.velocity

        # Second stage
        k_v[2] = self.physics.get_acceleration( (self.spacecraft.position + (self.config.time_step_size / 2.0)*k_r[1]), 
                                         (self.spacecraft.velocity + k_v[1] * (self.config.time_step_size / 2.0)) )
        k_r[2] = self.spacecraft.velocity + k_v[1] * (self.config.time_step_size / 2.0)

        # Third stage
        k_v[2] = self.physics.get_acceleration( (self.spacecraft.position + (self.config.time_step_size / 2.0)*k_r[2]), 
                                         (self.spacecraft.velocity + k_v[2] * (self.config.time_step_size / 2.0)) )
        k_r[3] = self.spacecraft.velocity + k_v[2] * (self.config.time_step_size / 2.0)

        # Fourth stage
        k_v[2] = self.physics.get_acceleration( (self.spacecraft.position + (self.config.time_step_size)*k_r[3]), 
                                         (self.spacecraft.velocity + k_v[3] * self.config.time_step_size) )
        k_r[4] = self.spacecraft.velocity + k_v[3] * self.config.time_step_size

        return k_r, k_v

    def _store_state(self, time:float) -> None:
        """
        Stores the time, position, and velocity of the spacecraft for other analysis purposes.
        """
        self._times.append(time)
        self._position.append(self.spacecraft.position.copy())
        self._velocity.append(self.spacecraft.velocity.copy())
        

    def _check_surface_impact(self) -> bool:
        """
        Checks to see whether the distance from the center of the planet to the spacecrafts
        current position is less than its radius, and given its a sphere, that would mean
        it has "hit" the surface.
        
        """
        return (np.linalg.norm(self.spacecraft.position) <= self.planet.radius)
    
    def get_trajectory(self) -> List[np.ndarray]:
        """ 
        A public, safe way for the position history of the spacecraft that was stored, to be accessed
        for use in external applications.
        """
        return self._position

    def get_times(self) -> List[np.ndarray]:
        """ 
        A public, safe way for the time history of the simulation that was periodically stored, to be accessed
        for use in external applications.
        """
        return self._times


    # TODO: I believe this needs to be rewritten as the logic is flawed, or rather not complete.
    def _check_if_will_eventually_hit_planet(self) -> bool:
        return (np.linalg.norm(self.spacecraft.velocity)) < np.sqrt( ((6.674e-11) * self.planet.mass) / np.linalg.norm(self.spacecraft.position))
    

