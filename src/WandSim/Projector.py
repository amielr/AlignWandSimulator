from src.WandSim.Ray import *
from src.WandSim.PlotFunctions import *
import json
import numpy as np



with open('../src/config.json') as config_file:
    config = json.load(config_file)


def get_lattice_distance():
    return config["LatticeConst"]*1e-6


def get_rotation_matrix(Xangle, Yangle, Zangle):
    XangleInRadians = np.deg2rad(Xangle)
    YangleInRadians = np.deg2rad(Yangle)
    ZangleInRadians = np.deg2rad(Zangle)
    XangleSin = np.sin(XangleInRadians)
    XangleCos = np.cos(XangleInRadians)
    YangleSin = np.sin(YangleInRadians)
    YangleCos = np.cos(YangleInRadians)
    ZangleSin = np.sin(ZangleInRadians)
    ZangleCos = np.cos(ZangleInRadians)

    XrotationMatrix = np.array([
            [1, 0, 0],
            [0, XangleCos, -XangleSin],
            [0, XangleSin, XangleCos]
        ])

    YrotationMatrix = np.array([
            [YangleCos, 0, YangleSin],
            [0, 1, 0],
            [-YangleSin, 0, YangleCos]
        ])

    ZrotationMatrix= np.array([
        [ZangleCos, -ZangleSin, 0],
        [ZangleSin, ZangleCos, 0],
        [0, 0, 1]
    ])

    return np.matmul(np.matmul(XrotationMatrix, YrotationMatrix), ZrotationMatrix)

class Projector():

    projectorName = "Blue projector 1"
    center = np.array([0, 0, 0])
    direction = np.array([0, 0, 0])
    rotationDirection = np.array([0, 0, 0])  # todo: change from vector direction to angle direction
    projectorType = "projector_blue"
    wavelength = 450
    ParentRay = Ray((0, 0, 0), (0, 0, 1), 1)
    ProjectorRayList = []
    NoOfProjectors = 0
    NoOfProjectorRays = 0

    def __init__(self, _name, _center,_direction, _rotation, _wavelength, _type):
        self.projectorName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        self.wavelength = 0 if _wavelength is None else _wavelength*1e-9
        self.projectorType = "noType" if _type is None else _type
        self.central_parent_ray()
        return

    def __str__(self):
        return "Projector Name: %s - Origin x %s, y %s , z %s - Direction x %s, y %s , z %s - Wavelength: %s, NoOfProj: %s"\
               % (self.projectorName, self.center[0], self.center[1], self.center[2],
                  self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2],
                  self.wavelength, self.NoOfProjectors)

    def central_parent_ray(self):
        self.ParentRay = Ray((self.center[0], self.center[1], self.center[2]),
                             (self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2]), 1, self)
        self.NoOfProjectorRays += 1
        Projector.NoOfProjectorRays += 1
        # print(self.ParentRay)
        return

    def get_grating_equation_angle(self, order):
        gratingdistance = get_lattice_distance()
        angle = math.asin(order*self.wavelength/gratingdistance)
        angle = math.degrees(angle)
        return angle

    def get_ray_angle_direction(self, facets, order, suborder):
        basisangle = 360/facets
        rotatingangle = basisangle/order
        rotationangle = rotatingangle * suborder
        print(rotationangle)
        # get_rotation_matrix(rotationangle, 'z')
        return rotationangle

    def addray(self, ray, raylist):
        raylist.append(ray)
        Projector.NoOfProjectorRays += 1
        self.NoOfProjectorRays += 1
        return raylist

    def generate_projector_rays(self, order):
        centraldirection = np.array([self.direction[0], self.direction[1], self.direction[2]])
        directionlist = [centraldirection]  # get central ray
        for gratingorderindex in range(1, order + 1):                         # create zero order column
            xangle = self.get_grating_equation_angle(gratingorderindex)
            xrotated = np.matmul(get_rotation_matrix(xangle, 0, 0), centraldirection)
            zrotated = np.matmul(get_rotation_matrix(0, 0, -60), xrotated)
            differencevec = zrotated - xrotated
            directionlist.append(xrotated)
            for j in range(1, gratingorderindex):                              # create suborder values
                directionlist.append(xrotated + (j*differencevec/gratingorderindex))
        print(len(directionlist))

        fulldirectionlist = []
        fulldirectionlist.extend(directionlist)
        newdirectionlist = []


        for j in range(1, 6):      # rotate around each quadrant/septant
            for direction in directionlist:
                # print(direction)
                newdirectionlist.append(np.matmul(get_rotation_matrix(0, 0, -60*j), direction))

        fulldirectionlist.extend(newdirectionlist)
        print(len(fulldirectionlist))
        npraylist = np.vstack(fulldirectionlist)
        print(len(npraylist))
        nplist = np.unique(npraylist, axis=0)
        print(len(nplist))


        finaldirections = np.matmul(get_rotation_matrix(self.rotationDirection[0],self.rotationDirection[1],self.rotationDirection[2]), nplist.T).T

        plot_scatter(finaldirections)
        return





#rotatedXYZ = np.matmul(get_rotation_matrix(angle, direction), stackFlattenXYZ)