import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_scatter(name, data):
    xcoords, ycoords, zcoords = data.T
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(name)
    plt.scatter(xcoords, ycoords)
    plt.savefig(str(name)+".jpg")
    plt.show(block=True)
    return


def plot_projector_ray_locations_scatter(projector):
    rayLocationList = []
    print(projector.NoOfProjectorRays)
    print(len(projector.ProjectorRayList))
    for ray in projector.ProjectorRayList:
        rayLocationList.append(ray.Origin)
    npraylocationlist = np.vstack(rayLocationList)
    xcoords, ycoords, zcoords = npraylocationlist.T

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(projector.projectorName)
    plt.scatter(xcoords, ycoords)

    plt.savefig(str(projector.projectorName) + "_raylocations"+ ".jpg")
    plt.show(block = True)
    return

def plot_quiver(rayList, title):
    Origins, Directions =  rayList[0].Origin, rayList[0].Direction
    colours = []
    for ray in rayList:
        Origins = np.vstack((Origins, ray.Origin))
        Directions = np.vstack((Directions, ray.Direction))
        colours.append(str(ray.ParentSource.projectorName)[0])


    #print(colours)
    X, Y, Z = Origins.T
    U, V, W = Directions.T

    #X, Y, Z, U, V, W = zip(*soa)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)
    ax.quiver(X, Y, Z, U, V, W, length=20, arrow_length_ratio=0.05, color=colours)
    ax.set_xlim(-2, 18)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-30, 3.3)
    plt.show(block = True)
