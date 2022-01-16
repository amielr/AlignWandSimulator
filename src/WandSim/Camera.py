from src.WandSim.Ray import *
from src.WandSim.PlotFunctions import *
from src.WandSim.Projector import get_rotation_matrix
from src.WandSim.WindowLens import *
import json
import numpy as np

with open('../src/config.json') as config_file:
    config = json.load(config_file)


class Camera():

    cameraName = "Camera 1"
    center = np.array([0, 0, 0])
    direction = np.array([0, 0, 0])
    rotationDirection = np.array([0, 0, 0])
    cameraLocalToWorld = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    worldToCamera = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    PixelXsize = 450
    PixelYsize = 0
    NoOfXPixels = 0
    NoOfYPixels = 0
    AperatureAngle = 0
    CameraDotRayList = []
    NoOfCameras = 0

    def __init__(self, _name, _center, _direction, _rotation, _type):
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        #self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.cameraType = "noType" if _type is None else _type
        self.set_Camera_to_World_Transformation()
        self.worldToCamera = np.linalg.inv(self.cameraLocalToWorld)
        #self.NoOfProjectors += 1
        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s cameraLocalToWorld - %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection, self.cameraLocalToWorld)

    def set_Camera_to_World_Transformation(self):

        B = get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])
        B = np.vstack((B, self.center))
        B = np.hstack((B, np.array([[0], [0], [0], [1]])))
        self.cameraLocalToWorld = B

        Inverse = np.linalg.inv(self.cameraLocalToWorld)
        #print(Inverse)

        #print(self.cameraLocalToWorld)
        return

    #def set_World_to_Camera_Transformation(self):

    def get_fermat_parameters(self, ray, window):
        print("ray Origin", ray.Origin)
        print("camera center", self.center)
        DistanceD = np.linalg.norm(self.center[:2] - ray.Origin[:2])
        print(DistanceD)
        height = abs(self.center[2]-ray.Origin[2])
        y = window.Thickness
        x = height - y
        N1 = 1
        N2 = window.RefractiveIndexDictionary.get(str(ray.get_ray_wavelength()))
        return N1, N2, DistanceD, x, y

    def find_fermat_root(self,N1, N2, DistanceD, x, y ):
        z4 = math.pow(N1, 2) - math.pow(N2, 2)
        z3 = 2 * DistanceD * (math.pow(N2, 2) - math.pow(N1, 2))
        z2 = (math.pow(N1, 2) * math.pow(y, 2) + math.pow(N1, 2) * math.pow(DistanceD, 2) - math.pow(N2, 2) * math.pow(
            x, 2)
              - math.pow(N2, 2) * math.pow(DistanceD, 2))
        z1 = 2 * DistanceD * math.pow(N2, 2) * math.pow(x, 2)
        z0 = -math.pow(N2, 2) * math.pow(DistanceD, 2) * math.pow(x, 2)

        print([z4, z3, z2, z1, z0])

        FermatPolynomial = np.poly1d([z4, z3, z2, z1, z0])
        FermatRoots = FermatPolynomial.roots
        print(N1, N2, DistanceD, x, y)

        print(FermatPolynomial)
        print(FermatRoots)


        for root in FermatRoots:
            if abs(root) < DistanceD:
                print("This is the chosen distance: ", root)
            else:
                print("We threw this distance out: ", root, abs(root))

        return

    def fermatManager(self, ray, window):
        N1, N2, DistanceD, x, y = self.get_fermat_parameters(ray, window)

        self.find_fermat_root(N1, N2, DistanceD, x, y)

        return

    def get_incident_ray_angle(self, rayList):
        for ray in rayList:
            self.fermatManager(ray, window[0])
        return


