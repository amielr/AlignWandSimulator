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

def plot_xy_scatter(X,Y):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title("scatter XY")
    plt.scatter(X, Y,s=4)
    plt.grid(True, 'both', 'both')
    major_ticks_x = np.arange(0, 1920, 100)
    major_ticks_y = np.arange(0, 1080, 100)
    ax.set_xticks(major_ticks_x)
    ax.set_yticks(major_ticks_y)
    ax.set_xlim([0,1920])
    ax.set_ylim([0,1080])
    #plt.savefig(str(name) + ".jpg")
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
        print("origin is", ray.Origin)
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
    #x,y,z = ray.Origin
    fig = plt.figure()
    plt.subplot(projection='3d')

    # x = np.linspace(-1, 1, 10)
    # y = np.linspace(-1, 1, 10)
    # X, Y = np.meshgrid(x, y)
    # Z = 0.12861723162963065 * X + 0.0014024845304814665 * Y + 1.0964608113924048

    for ray in rays:
        x, y, z = [], [], []
        #print("we are in ray path line plot: ", ray.RayStoryCoordinates)
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


def plot_STL_object(mesh):
    # %%
    # getting vertices and triangles
    vert = np.asarray(mesh.vertices)
    tri = np.asarray(mesh.triangles)

    print("triangle data")
    print(mesh.triangles)
    print(tri)
    ax = plt.axes(projection='3d')
    x, y, z = vert[::100, 0], vert[::100, 1], vert[::100, 2]
    ax.plot_trisurf(x, y, z,
                    cmap='viridis', edgecolor='none');
    return
