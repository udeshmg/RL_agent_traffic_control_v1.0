import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
DEBUG_LEVEL = 1


class Display:

    def __init__(self):
        print("Setting up display")
        # plt.axis([0, 10, -1000, 1000])

    @staticmethod
    def plot(vehicle_data):
        plt.figure(2)
        plt.axis([0, 4, 0, 6])
        obj = ['1', '2', '3', '4']
        bar_list = plt.bar(obj, height=vehicle_data, align='center', width=0.8)
        bar_list[0].set_color('r')
        bar_list[1].set_color('g')
        bar_list[2].set_color('b')
        bar_list[3].set_color('y')
        plt.pause(0.05)
        plt.clf()

    @staticmethod
    def debug_info(string, level):
        if DEBUG_LEVEL < level:
            print(string)

    @staticmethod
    def figure(average_val, i, figure_num=1):
        plt.figure(figure_num)
        plt.scatter(i, average_val, edgecolors='r', c=None, s=1)

    @staticmethod
    def figure_time(average_val, i, figure_num=3):
        plt.figure(figure_num)
        plt.scatter(i, average_val, edgecolors='g', c=None, s=1)

    @staticmethod
    def plot3d(array2d):
        x = range(array2d.shape[1])
        y = range(array2d.shape[0])
        print('szie', x, y)
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid(x, y)

        # scaled = np.divide(array2d, np.amax(array2d))
        color_bar = ax.scatter(X, Y, array2d)
        ax.set_title('Q table')
        #cbar = plt.colorbar(color_bar)
        #cbar.set_label("Values (units)")
        plt.show()


