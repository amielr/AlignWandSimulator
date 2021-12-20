import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_scatter(data):
    xcoords, ycoords, zcoords = data.T
    plt.scatter(xcoords, ycoords)
    plt.show()
    return

def plot_scalar_field(xcoords, ycoords, zcoords):
    plt.contourf(xcoords, ycoords, zcoords, cmap='jet')

    plt.colorbar()
    plt.show()
    return

def plot_quiver(rayList):
    Origins, Directions =  rayList[0].Origin, rayList[0].Direction
    for ray in rayList:
        Origins = np.vstack((Origins, ray.Origin))
        Directions = np.vstack((Directions, ray.Direction))


    X, Y, Z = Origins.T
    U, V, W = Directions.T

    #X, Y, Z, U, V, W = zip(*soa)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, U, V, W, length=25, arrow_length_ratio=0.05)
    ax.set_xlim(-2, 18)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-30, 3.3)

    plt.show(block = True)