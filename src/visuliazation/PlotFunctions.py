import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
#from mpl_toolkits.mplot3d import Axes3D
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

def plot_xy_scatter(X,Y, XV, YV):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title("scatter XY")
    #plt.scatter(X, Y, s=4)

    plt.scatter(X, Y, s=6, c='b', marker="s", label='simulation')
    plt.scatter(XV, YV, s=4, c='g', marker="o", label='validation')

    plt.grid(True, 'both', 'both')
    major_ticks_x = np.arange(0, 1920, 100)
    major_ticks_y = np.arange(0, 1080, 100)
    ax.set_xticks(major_ticks_x)
    ax.set_yticks(major_ticks_y)
    ax.set_xlim([0, 960])
    ax.set_ylim([0, 540])
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


def plot_ray_locations(rays):
    rayLocationList = []
    for ray in rays:
        rayLocationList.append(ray.Origin)
    npraylocationlist = np.vstack(rayLocationList)
    xcoords, ycoords, zcoords = npraylocationlist.T

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$Z$')

    ax.scatter(xcoords, ycoords, zcoords)
    plt.show(block=True)
    return

def plot_ray_path_line(rays):
    fig = plt.figure()
    plt.subplot(projection='3d')
    for ray in rays:
        x, y, z = [], [], []
        #print("we are in ray path line plot our raystory is: ", ray.RayStoryCoordinates[:8])
        for rayCoordinates in ray.RayStoryCoordinates:
            #print(rayCoordinates)
            x.append(rayCoordinates[0])
            y.append(rayCoordinates[1])
            z.append(rayCoordinates[2])
        plt.plot(x, y, z)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show(block=True)
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot(x, y, z)
    # plt.show()


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
