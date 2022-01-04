from src.WandSim.Ray import *
from src.WandSim.PlotFunctions import *
import json
import math
import numpy as np





with open('../src/config.json') as config_file:
    config = json.load(config_file)


class Camera():

    cameraName = "Camera 1"
    center = np.array([0, 0, 0])
    direction = np.array([0, 0, 0])
    rotationDirection = np.array([0, 0, 0])
    cameraToWorld = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    worldToCamera = np.linalg.inv(cameraToWorld)
    PixelXsize = 450
    PixelYsize = 0
    NoOfXPixels = 0
    NoOfYPixels = 0
    AperatureAngle = 0
    CameraDotRayList = []
    NoOfCameras = 0

    def __init__(self, _name, _center, _direction, _rotation, _wavelength, _type):
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        #self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.projectorType = "noType" if _type is None else _type
        #self.NoOfProjectors += 1
        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection)

    def set_Camera_to_World_Transformation(self):

        return