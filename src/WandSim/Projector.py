from src.WandSim.Ray import *
import json
import numpy as np
import matplotlib.pyplot as plt



with open('../src/config.json') as config_file:
    config = json.load(config_file)


def get_lattice_distance():
    return config["LatticeConst"]*1e-6


def get_rotation_matrix(angle, direction):
    angleInRadians = np.deg2rad(angle)
    angleSin = np.sin(angleInRadians)
    angleCos = np.cos(angleInRadians)

    if direction == 'x':
        return [
            [1, 0, 0],
            [0, angleCos, -angleSin],
            [0, angleSin, angleCos]
        ]

    if direction == 'y':
        return [
            [angleCos, 0, angleSin],
            [0, 1, 0],
            [-angleSin, 0, angleCos]
        ]

    return [
        [angleCos, -angleSin, 0],
        [angleSin, angleCos, 0],
        [0, 0, 1]
    ]

class Projector():

    projectorName = "Blue projector 1"
    center = Vector(0, 0, 0)
    direction = Vector(0, 0, 0)
    rotationDirection = Vector(0, 0, 0)  # todo: change from vector direction to angle direction
    projectorType = "projector_blue"
    wavelength = 450
    ParentRay = Ray((0, 0, 0), (0, 0, 1), 1)
    ProjectorRayList = []
    NoOfProjectors = 0
    NoOfProjectorRays = 0

    def __init__(self, _name, _center,_direction, _rotation, _wavelength, _type):
        self.projectorName = "noName" if _name is None else _name
        self.center = Vector(0, 0, 0) if _center is None else Vector(_center[0], _center[1], _center[2])
        self.direction = Vector(0, 0, 0) if _direction is None else Vector(_direction[0], _direction[1], _direction[2])
        self.rotationDirection = Vector(0, 0, 0) if _rotation is None else Vector(_rotation[0], _rotation[1], _rotation[2])
        self.wavelength = 0 if _wavelength is None else _wavelength*1e-9
        self.projectorType = "noType" if _type is None else _type
        self.central_parent_ray()
        return

    def __str__(self):
        return "Projector Name: %s - Origin x %s, y %s , z %s - Direction x %s, y %s , z %s - Wavelength: %s, NoOfProj: %s"\
               % (self.projectorName, self.center.get_x(), self.center.get_y(), self.center.get_z(),
                  self.rotationDirection.get_x(), self.rotationDirection.get_y(), self.rotationDirection.get_z(),
                  self.wavelength, self.NoOfProjectors)

    def central_parent_ray(self):
        self.ParentRay = Ray((self.center.x, self.center.y, self.center.z),
                             (self.rotationDirection.x, self.rotationDirection.y, self.rotationDirection.z), 1, self)
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
        directionlist = [np.array([self.direction.get_x(), self.direction.get_y(), self.direction.get_z()])]  # get central ray
        projectordirection = directionlist[0]
        for orderindex in range(1, order + 1):                         # create zero order column
            xangle = self.get_grating_equation_angle(orderindex)
            xrotated = np.matmul(get_rotation_matrix(xangle, 'x'), projectordirection)
            zrotated = np.matmul(get_rotation_matrix(-60, 'z'), xrotated)
            differencevec = zrotated - xrotated
            directionlist.append(xrotated)
            for j in range(1, orderindex):                              # create suborder values
                directionlist.append(xrotated + (j*differencevec/orderindex))
        print(len(directionlist))

        fulldirectionlist = []
        fulldirectionlist.extend(directionlist)
        newdirectionlist = []


        for j in range(1, 6):      # rotate around each quadrant/septant
            for direction in directionlist:
                # print(direction)
                newdirectionlist.append(np.matmul(get_rotation_matrix(-60*j, 'z'), direction))

        fulldirectionlist.extend(newdirectionlist)
        print(len(fulldirectionlist))
        nplist = np.vstack(fulldirectionlist)
        print(len(nplist))
        nplist = np.unique(nplist, axis=0)
        print(len(nplist))

        x, y, z = nplist.T

        # plot our list in X,Y coordinates
        plt.scatter(x, y)
        plt.show()


        return





#rotatedXYZ = np.matmul(get_rotation_matrix(angle, direction), stackFlattenXYZ)