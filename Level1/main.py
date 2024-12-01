# Level 1 of the reentry model:
#   - treat the spacecraft as a point mass
#   - No atmosphere on Earth
#   - Assuming the Earth is a perfect sphere/circle
#   - Simple ballistics trajectory

# Author: Tyler Allen
# Date started: 17 November 2024


import yaml


from src.spacecraft import Spacecraft
from src.planet import Planet
from src.simulation import Simulation
from src.plotting import Plotting

from src.config.configuration_manager import ConfigurationManager



def main():

    config = ConfigurationManager("config/config.yaml")
    
    
    spacecraft = Spacecraft(config.spacecraft)
    planet = Planet(config.planet)
    simulation = Simulation(config.simulation,
                            spacecraft = spacecraft,
                            planet = planet)
    
    plotter = Plotting()


    # Run the Runge-Kutta orbital calculation
    simulation.run()



    # Plot the results of the simulation, namely the position of the spacecraft
    plotter.simple_orbital_trajectory(simulation.get_trajectory(), display_plot=True)

    

if __name__ == "__main__":
    main()