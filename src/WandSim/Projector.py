from src.WandSim.Ray import *
import json
import math
import numpy as np

with open('../src/System_Parameters/config.json') as config_file:
    config = json.load(config_file)

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
    rotationDirection = np.array([0, 0, 0])
    projectorType = "projector_blue"
    wavelength = 450
    AllProjectorRaysList = []
    NoOfProjectors = 0
    NoOfProjectorRays = 0
    gratingOrder = 0
    LatticeConstant = 0

    def __init__(self, _name, _center, _direction, _rotation, _wavelength, _type, _gratingOrder, _LatticeConstant):
        self.projectorName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        #self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.ProjectorRayList = []
        self.wavelength = 0 if _wavelength is None else _wavelength*1e-9
        self.projectorType = "noType" if _type is None else _type
        self.gratingOrder = 0 if _gratingOrder is None else _gratingOrder
        self.LatticeConstant = 0 if _LatticeConstant is None else _LatticeConstant
        self.central_parent_ray()
        #self.NoOfProjectors += 1
        return

    def __str__(self):
        return "Projector Name: %s - Origin %s, - Direction  %s, - Rotation %s - Wavelength: %s, NoOfProj: %s"\
               % (self.projectorName, self.center, self.direction,
                  self.rotationDirection,self.wavelength, self.NoOfProjectors)

    def central_parent_ray(self):
        self.ParentRay = Ray(self.center, self.direction, 1, self)
        #self.NoOfProjectorRays += 1
        #Projector.NoOfProjectorRays += 1
        return

    def get_lattice_distance(self):
        return self.LatticeConstant * 1e-6 * np.cos(np.pi/6)

    def get_grating_equation_angle(self, order):
        gratingdistance = self.get_lattice_distance()
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

    def build_first_hextant(self, order):
        centraldirection = np.array([self.direction[0], self.direction[1], self.direction[2]])
        directionlist = []  # get central ray
        raylist = []
        #raylist.append(Ray(self.center, self.direction, 1, self, 0, 0))
        for gratingorderindex in range(1, order + 1):  # create zero order column
            xangle = self.get_grating_equation_angle(gratingorderindex)
            xrotated = np.matmul(get_rotation_matrix(xangle, 0, 0), centraldirection.T)
            zrotated = np.matmul(get_rotation_matrix(0, 0, -60), xrotated)
            differencevec = zrotated - xrotated
            directionlist.append(xrotated)
            raylist.append(Ray(self.center, xrotated, 1, self, gratingorderindex, 0))

            for j in range(1, gratingorderindex):  # create suborder values
                directionlist.append(xrotated + (j * differencevec / gratingorderindex))
                raylist.append(Ray(self.center, (xrotated + (j * differencevec / gratingorderindex)), 1, self, gratingorderindex, j))
        return directionlist, raylist

    def build_remaining_hextants(self, directionlist):
        centraldirection = np.array([self.direction])
        newdirectionlist = []
        for j in range(1, 6):  # rotate around each quadrant/hextant
            for direction in directionlist:
                # print(direction)
                newdirectionlist.append(np.matmul(get_rotation_matrix(0, 0, -60 * j), direction))
        newdirectionlist.append(centraldirection)
        return newdirectionlist

    def build_remaining_hextant_rays(self, raylist):
        centraldirection = np.array(self.direction)
        newraylist = []
        for j in range(1, 6):  # rotate around each quadrant/hextant
            for ray in raylist:
                newraylist.append(Ray(self.center, np.matmul(get_rotation_matrix(0, 0, -60 * j), ray.Direction), 1, self, ray.IndexI, ray.IndexJ + ray.IndexI*j))
                # print(direction)
        newraylist.append(Ray(self.center, centraldirection, 1, self, 0, 0))
        return newraylist

    def generate_projector_rays(self):

        directionlist, raylist = self.build_first_hextant(self.gratingOrder)                  # get the directions from grating of projector of first hextant
        newdirectionlist = self.build_remaining_hextants(directionlist)  # get the directions of the remaining hextants
        newraylist = self.build_remaining_hextant_rays(raylist)
        directionlist.extend(newdirectionlist)                           # full direction list of a single projector
        raylist.extend(newraylist)

        rotateddirectionlist = [np.matmul(raydirection, get_rotation_matrix(0, 0, -30)) for raydirection in directionlist]
        #rotatedraylist = [ray.Direction = (np.matmul(ray.Direction, get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2]-30))) for ray in raylist]

        for ray in raylist:
            ray.Direction = np.matmul(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2]-30),ray.Direction)

        npraylist = np.vstack(rotateddirectionlist)
        nplist = np.unique(npraylist, axis=0)
        #print(len(nplist))
        # Change directions to suit the projector direction
        finaldirections = np.matmul(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2]), nplist.T).T

        # Turn directions into rays - Origin, Direction, Amplitude combinations
        # for direction in finaldirections:
        #     self.ProjectorRayList.append(Ray(self.center, direction, self.ParentRay.get_amplitude()/len(finaldirections), self))
        #     Projector.AllProjectorRaysList.append(Ray(self.center, direction, self.ParentRay.get_amplitude()/len(finaldirections), self))
        #     self.NoOfProjectorRays += 1
        #     Projector.NoOfProjectorRays += 1

        self.ProjectorRayList = raylist
        Projector.AllProjectorRaysList.extend(raylist)
        self.NoOfProjectorRays = len(raylist)
        Projector.NoOfProjectorRays = len(raylist)

        #plot_scatter(self.projectorName, finaldirections)
        print(self)
        return

    def get_projector_ray_origins(self):
        origins = np.array(self.center)
        for ray in self.ProjectorRayList:
            origins = np.vstack((origins, ray.Origin))
        return origins

    def get_projector_ray_directions(self):
        directions = np.array(self.direction)
        for ray in self.ProjectorRayList:
            directions = np.vstack((directions, ray.Direction))
        return directions
