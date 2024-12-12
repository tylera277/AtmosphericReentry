# Level 2

# Author: Tyler Allen
# Date started: 02 December 2024


import yaml


from src.spacecraft import Spacecraft
from src.planet import Planet
from src.simulation import Simulation
from src.plotting import Plotting
from src.physics import Physics

from src.config.configuration_manager import ConfigurationManager



def main():

    config = ConfigurationManager("config/config.yaml")
    
    
    spacecraft = Spacecraft(config.spacecraft)
    planet = Planet(config.planet)
    physics = Physics(config.physics, planet, spacecraft)
    simulation = Simulation(config.simulation,
                            spacecraft = spacecraft,
                            planet = planet,
                            physics= physics)
    
    plotter = Plotting()


    # Run the Runge-Kutta orbital calculation
    simulation.run()



    # Plot the results of the simulation, namely the position of the spacecraft
    plotter.simple_orbital_trajectory(simulation.get_trajectory(), display_plot=False)
    plotter.simple_2d_plot(simulation.get_trajectory(), display_plot=False)

    plotter.plot_velocity_distribution(simulation.get_velocities(), 
                                       simulation.get_times(),
                                       display_plot= True,
                                       save_plot= True)

if __name__ == "__main__":
    main()