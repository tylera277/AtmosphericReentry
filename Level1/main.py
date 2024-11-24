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


def main():

    try:
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)

    except Exception as e:
        print(f"Failed to laod configuration file: {e}")

    try:
        spacecraft = Spacecraft(config['spacecraft'])
        planet = Planet(config['planet'])
        simulation = Simulation(config['simulation'],
                                spacecraft = spacecraft,
                                planet = planet)
        plotter = Plotting()

        results = simulation.run()

        # Plot the results of the simulation, namely the position
        plotter.simple_orbital_trajectory(results)

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()