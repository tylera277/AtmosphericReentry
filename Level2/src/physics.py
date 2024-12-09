

import numpy as np

from .config.physics_config import PhysicsConfig
from .spacecraft import Spacecraft
from .planet import Planet


class Physics:

    def __init__(self, config: PhysicsConfig, planet: Planet, spacecraft: Spacecraft):
        self.config = config
        self.planet = planet
        self.spacecraft = spacecraft

        # Parameters set by user for a specific spacecraft
        self.cross_sectional_area = self.spacecraft.cross_sect_area
        self.drag_coefficient = self.spacecraft.drag_coefficient
        self.mass = self.spacecraft.mass


    def get_acceleration(self, spacecraft_position: np.ndarray, spacecraft_velocity: np.ndarray):
        """
        Houses all of the calls to the acceleration calculations the simulation takes into account.
        Specified explicitly by the user in the config file.

        Args:
            spacecraft_position (np.ndarray): a vector for the position of the spacecraft
            spacecraft_velocity (np.ndarray): a vector for the velocity of the spacecraft

        Returns:
            np.ndarray: the sum of all of the accelerations calculated for the spacecraft given its current state.
        """
        
        # Local variable which will hold the force thats calculated.
        total_acceleration = np.zeros((3))

        # Gravity (included by default)
        total_acceleration += self.get_gravity(spacecraft_position)
    
        # Drag
        if self.config.include_drag:
            total_acceleration += self.get_drag(spacecraft_position, spacecraft_velocity)
        
        # NOTE(TA 07dec2024): add extra forces the craft could experience here later on

        return total_acceleration


    def get_gravity(self, spacecraft_position: np.ndarray):
        """
        Handles calling the planets classes calculate_gravity function in order to calculate
        the gravity that the object feels at a particular position.

        Args:
            spacecraft_position (np.ndarray): a vector for the position of the spacecraft

        Returns:
            np.ndarray: acceleration due to gravity the spacecraft is experiencing.
        """
        return self.planet.calculate_gravity(spacecraft_position)
    

    def get_drag(self, spacecraft_position: np.ndarray, spacecraft_velocity: np.ndarray):
        
        """
        Calculates the drag on the spacecraft using its own state as well as the atmospheric density
        model the user specified in the config file.

        Args:
            spacecraft_position (np.ndarray): a vector for the position of the spacecraft
            spacecraft_velocity (np.ndarray): a vector for the velocity of the spacecraft

        Returns:
            np.ndarray: acceleration due to drag the spacecraft is experiencing.
        """

        # The air density at the crafts altitude, if any, and using the model that the
        # user specified in the config file.
        air_density = self.planet.get_atmospheric_density(spacecraft_position)

        velocity_magnitude = np.linalg.norm(spacecraft_velocity)

        # Drag works in the opposite direction of motion. So this unit vector is used to get
        # the directional aspect of the motion so we can tell how that drag force is divied up 
        # along the three cartesian coordinates.
        unit_vector_opposite_to_velocity = -spacecraft_velocity / np.linalg.norm(spacecraft_velocity)

        # Actual drag force, taking in all the variables previously retrieved & calculated
        drag_force = (0.5 * self.drag_coefficient * self.cross_sectional_area * 
                      air_density * (velocity_magnitude**2) * 
                      unit_vector_opposite_to_velocity)
        

        drag_acceleration = drag_force / self.mass

        
        return drag_acceleration