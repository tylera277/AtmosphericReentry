
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd


class Plotting:
    """
    A class to house all plotting related materials needed at times throughout the project.
    
    """

    def simple_orbital_trajectory(self, list_of_positions: List[np.ndarray], display_plot: bool):
        """
        Plotting a list of the spacecrafts positions calculated over the simulation,
        and adding in a blank sphere to mimic the Earth.

        Args:
            list_of_positions (list): the positions (x,y,z) of the spacecraft that were saved
            display_plot (bool): stating whether you want the plot to show. True for yes, False for no.
        
        """

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')


        # Making a sphere to represent the Earths surface
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x_sphere = 6371000 * np.outer(np.cos(u), np.sin(v))
        y_sphere = 6371000 * np.outer(np.sin(u), np.sin(v))
        z_sphere = 6371000 * np.outer(np.ones(np.size(u)), np.cos(v))
    
        ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.3)

        # Extracting the x,y,z positions from the list received
        x_positions = [item[0] for item in list_of_positions]
        y_positions = [item[1] for item in list_of_positions]
        z_positions = [item[2] for item in list_of_positions]

        ax.set_xlim(-1e7, 1e7)
        ax.set_ylim(-1e7, 1e7)

        ax.plot(x_positions, y_positions, z_positions)

        if display_plot:
            plt.show()

    def crash_point_latLon_on_actual_earth(self, crash_location_on_sphere: np.ndarray, time_elapsed: float):
        """
        Mathematically determining the latitude and longitude of the crash spot on the actual Earth.

        The simulation reference frame is oriented the same as an Earth based one, where its tilted
        23.5 degrees, and starting at time=0, theyre x-axes are pointing in the same direction. The x-axis
        for the Earth based frame is 0 degrees longitude.
        So with the information of how long the simulation ran, I rotate the Earth by that amount of time about the z-axis 
        in order to get where the spacecraft would have hit on the actual Earth.

        Args:
            crash_location_on_sphere (np.ndarray): the vector which represents where the craft hit the blank sphere
                that has the same radius of the Earth.
            time_elapsed (float): the time from when the simulation began to when it was terminated.
        """

        earths_tilt_degrees = 23.5  
        earths_rotation_rate = 360 / (24*60*60)  # degrees/second
    
        point_on_earth = np.zeros(3)
        x_sphere, y_sphere, z_sphere = crash_location_on_sphere[0], crash_location_on_sphere[1], crash_location_on_sphere[2]

        # Total amount the earth rotated in that time, in radians
        total_rotation = np.radians(earths_rotation_rate * time_elapsed)

        # The point on the earth which is where that collision point would be equal to.
        # Connecting a non rotating reference frame to earths actual ref. frame
        point_on_earth[0] = x_sphere * np.cos(total_rotation) - y_sphere * np.sin(total_rotation)
        point_on_earth[1] = x_sphere * np.cos(total_rotation) + y_sphere * np.cos(total_rotation)
        point_on_earth[2] = z_sphere

        r = np.linalg.norm(point_on_earth)
        latitude = np.asin(point_on_earth[2] / r)
        longitude = np.atan2(point_on_earth[1], point_on_earth[0])

        


        return np.rad2deg(latitude), np.rad2deg(longitude)
    


    def plot_point_on_map(self, latitude:float, longitude:float, display_plot:bool):
        """
        At least for now, this function plots the crash point on an actual map of the Earth.

        Args:
            latitude (float): the latitude of the crash location on the Earth.
            longitude (float): the longitude of the crash location on the Earth.
            display_plot (bool): a conditional stating whether the user wants the plot to display.

        TODO: I would like to eventually add a dotted line on the same plot so that 
        one can see its trajectory before it hits. A spherical or standard mercadian underlying plot,
        not sure which one yet though.
        
        """

        columns = ['latitude', 'longitude']
        data = [(latitude, longitude)]

        empty = pd.DataFrame(data, columns=columns)
        
        fig = px.scatter_map(empty,
                             lat=empty['latitude'],
                             lon=empty['longitude'],
                             zoom=1)
        
        if display_plot:
            fig.show()


