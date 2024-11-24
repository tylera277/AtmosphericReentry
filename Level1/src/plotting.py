
import matplotlib.pyplot as plt


class Plotting:
    def __init__(self):
        pass


    def simple_orbital_trajectory(self, list_of_positions):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        #print(list_of_positions)
        ax.plot(list_of_positions[:][0], list_of_positions[:][1], list_of_positions[:][2])
        plt.show()

