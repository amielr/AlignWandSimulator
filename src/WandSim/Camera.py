from src.WandSim.Ray import *
from src.WandSim.PlotFunctions import *
from src.WandSim.Projector import get_rotation_matrix
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
    #worldToCamera = np.linalg.inv(cameraLocalToWorld)
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
        #self.NoOfProjectors += 1
        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s cameraLocalToWorld - %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection, self.cameraLocalToWorld)

    def set_Camera_to_World_Transformation(self):

        B = get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])
        B = np.vstack((B, self.center))
        B = np.hstack((B,np.array([[0],[0],[0],[1]])))
        self.cameraLocalToWorld = B
        #print(self.cameraLocalToWorld)
        return