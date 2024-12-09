
import numpy as np

from .config.planet_config import PlanetConfig


class Planet:
    """
    All parameters pertaining to the planet that youre wanting to use.
    Written so that any planet conditions and characteristics can be used.
    """
    def __init__(self, config: PlanetConfig):
        
        # Going to try to use this to access atmospheric model specific parameters
        # that are only relevant in their specific contexts.
        # (i.e. only when a particular model is called, should you get the parameters
        # it specifically requires)
        self.config = config

        # Default planet parameters that are used throughout program
        self.mass = config.mass
        self.radius = config.radius
        self.atmospheric_density_model = config.atmospheric_model

    def calculate_gravity(self, position_of_object: np.ndarray) -> np.ndarray:
        """
        Calculates, given the position of the spacecraft, the gravitational force
        it would feel from this planet.
        Its assuming that the planet is at the origin of the coordinate frame that
        is being used.
        
        Args:
            position_of_object: the array specifying the position of the spacecraft currently.

        Raises:
            ZeroDivisionError: In case the simulation calculates the position of the 
                spacecraft to be the origin. If happens, something fundamentally wrong
                in the code happened.
        
        Returns:
            force of gravity (np.ndarray): the value of the gravity force which the craft 
            feels at a specific moment.
        """


        # the gravitational constant
        G = 6.67430e-11

        dist = np.linalg.norm(position_of_object)

        if dist == 0:
            raise ZeroDivisionError("Position vector cannot be zero.")
        
        return -G * self.mass * position_of_object / (dist**3)


    def get_atmospheric_density(self, position_of_object: np.ndarray):
        """
        Calls the atmospheric density model represented by what the user 
        specified in the config file.
        """

        if self.atmospheric_density_model == "exponential_decay":
            return self.atmosphere_exponential_decay(position_of_object)
        
        
        raise ValueError("You did not select a currently programmed atmospheric model.")
    

    def atmosphere_exponential_decay(self, position_of_object: np.ndarray):
        """
        The exponential decay model for determining the  air density as a 
        function of altitude for a planet.
        Simplest model.

        Args:
            position_of_object (np.ndarray): the position of the spacecraft
        
        Returns:
            air_density (float): the scalar value of the density of the air 
                at the specified altitude. (in kg/m^3)
        
        """
        scale_height = self.config.scale_height        
        sea_level_density = self.config.sea_level_density


        # The distance the spacecraft is from the surface of the planet
        # (assuming the planet is a perfect sphere a.t.m.)
        height_from_surface = np.linalg.norm(position_of_object) - self.radius
        print("height: ", height_from_surface)

        density = sea_level_density * np.exp(-height_from_surface/scale_height)

        return density