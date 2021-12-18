import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import griddata
import numpy as np
import json
from matplotlib import cm
from matplotlib.ticker import LinearLocator


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