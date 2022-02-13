from src.WandSim.Ray import *
from src.WandSim.PlotFunctions import *
from src.WandSim.Projector import get_rotation_matrix
from src.WandSim.WindowLens import *
from copy import deepcopy
from src.WandSim.WandSimulatorManager import *
import json
import numpy as np

#import cupy as np

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
    #Camerawindow = WindowLens()

    def __init__(self, _name, _center, _direction, _rotation, _type):
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        #self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.cameraType = "noType" if _type is None else _type
        #self.window = WindowLens()
        #self.set_Camera_to_World_Transformation()
        #self.worldToCamera = np.linalg.inv(self.cameraLocalToWorld)
        #self.NoOfProjectors += 1
        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s cameraLocalToWorld - %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection, self.cameraLocalToWorld)

    def reorder_list_from_closest_to_furthest(self, ray, surfaceList):
        distanceList = []
        flag = False
        for surface in surfaceList:
            distance = np.linalg.norm(ray.Origin - surface.CenterPoint)
            distanceList.append(distance)
            print(str(surface.Name) + " distance from ray origin to surface camera module: " + str(distance))

        sortedSurfacesList = [x for _, x in sorted(zip(distanceList, surfaceList))]
        [print(surfaceholder.CenterPoint) for surfaceholder in sortedSurfacesList]
        return sortedSurfacesList



    def get_initial_intersection_points_from_surface_to_camera(self, rayList, windowsList):

        self.cameraRayList = deepcopy(rayList)

        print("we are here", self.cameraRayList)
        for ray in self.cameraRayList:
            ray.Direction = ray.normalize(self.center - ray.Origin)
            #print("ray surface camera direction", ray.Direction, ray.Origin)
            sortedwindowsList = self.reorder_list_from_closest_to_furthest(ray, windowsList)

            for window in sortedwindowsList:
                sortedSurfaceList = self.reorder_list_from_closest_to_furthest(ray, window.surfaceList)

                ray.IsRayInWindow = not ray.IsRayInWindow
                window.ray_window_refractive_registration(ray)
                for surface in sortedSurfaceList:
                    print("the closest surface to ray from camera mode is : " + str(surface.Name) + " " + str(surface.CenterPoint))

                    ray.ray_surface_intersection(surface)
                    ray.IsRayInWindow = not ray.IsRayInWindow
                    window.ray_window_refractive_registration(ray)

                print(self.cameraName, " ray surface intersection", ray.Origin)

            ray.IsRayInWindow = not ray.IsRayInWindow
            window.ray_window_refractive_registration(ray)
            ray.set_origin(self.center)
            ray.write_the_story(self.cameraName, ray.Origin, ray.RayMuuValue)

        return self.cameraRayList





    def determine_time_distance_path_length(self):
        distance = 0
        for ray in self.cameraRayList:
            print("ray to be determined", ray)
            distancesList = np.linalg.norm(np.diff(ray.RayStoryCoordinates, axis=0), axis=1)
            print("distance list: ", distancesList)
            ray.RayrefractiveIndexList = np.delete(ray.RayrefractiveIndexList, 0)
            print("refractive index list = ", ray.RayrefractiveIndexList)
            ray.RayPathDistance = np.sum(distancesList)
            print("total path distance before index correction = ", ray.RayPathDistance)
            products = [a * b for a, b in zip(distancesList, ray.RayrefractiveIndexList)]
            ray.RayPathDistance = np.sum(products)
            print("total path distance after index correction= ", ray.RayPathDistance)
        return

    def optimize_Camera_rays(self):
        self.determine_time_distance_path_length()
        return

    # def get_fermat_parameters(self, ray, window):
    #     print("ray Origin", ray.Origin)
    #     print("camera center", self.center)
    #     DistanceVector = self.center[:2] - ray.Origin[:2]
    #     DistanceD = np.linalg.norm(self.center[:2] - ray.Origin[:2])
    #     print(DistanceD)
    #     height = abs(self.center[2]-ray.Origin[2])
    #     y = window.Thickness
    #     x = height - y
    #     N1 = 1
    #     N2 = window.RefractiveIndexDictionary.get(str(ray.get_ray_wavelength()))
    #     return N1, N2, DistanceD, DistanceVector, x, y
    #
    # def find_fermat_root(self,N1, N2, DistanceD, x, y ):
    #     z4 = math.pow(N1, 2) - math.pow(N2, 2)
    #     z3 = 2 * DistanceD * (math.pow(N2, 2) - math.pow(N1, 2))
    #     z2 = (math.pow(N1, 2) * math.pow(y, 2) + math.pow(N1, 2) * math.pow(DistanceD, 2) - math.pow(N2, 2) * math.pow(
    #         x, 2)
    #           - math.pow(N2, 2) * math.pow(DistanceD, 2))
    #     z1 = 2 * DistanceD * math.pow(N2, 2) * math.pow(x, 2)
    #     z0 = -math.pow(N2, 2) * math.pow(DistanceD, 2) * math.pow(x, 2)
    #
    #     #print([z4, z3, z2, z1, z0])
    #
    #     FermatPolynomial = np.poly1d([z4, z3, z2, z1, z0])
    #     FermatRoots = FermatPolynomial.roots
    #     #print(N1, N2, DistanceD, x, y)
    #
    #     #print(FermatPolynomial)
    #     #print(FermatRoots)
    #
    #
    #     for root in FermatRoots:
    #         if abs(root) < DistanceD:
    #             print("This is the chosen distance: ", root)
    #             return root
    #         # else:
    #         #     print("We threw this distance out: ", root, abs(root))
    #
    #     return
    #
    # def fermatManager(self, rayList, window):
    #     rootList = []
    #     self.cameraRayList = deepcopy(rayList)
    #     for ray in self.cameraRayList:
    #         N1, N2, DistanceD, DistanceVector, x, y = self.get_fermat_parameters(ray, window)
    #         rootList.append(self.find_fermat_root(N1, N2, DistanceD, x, y))
    #         DistanceVector = DistanceVector / np.linalg.norm(DistanceVector)
    #         print("vector Direction: ", DistanceVector)
    #         location = ray.Origin[:2] + DistanceVector*DistanceD
    #         print("vector location: ", location)
    #         print("comparison camera location: ", self.center)
    #         windowincident = ray.Origin[:2] + DistanceVector*rootList[-1]
    #         windowincident = np.insert(windowincident, 2, ray.Origin[2]+x)
    #         print("window location root:", windowincident)
    #         rayDirection = windowincident - ray.Origin
    #         print("ray direction: ", rayDirection)
    #         ray.set_origin(self.center)
    #         ray.set_direction(rayDirection)
    #         ray.write_the_story(self.cameraName, 0, 0, ray.Direction)
    #     print(len(self.cameraRayList))
    #     plot_quiver(self.cameraRayList, self.cameraName)
    #     print(rootList)
    #     print("End of camera: ", self.cameraName)
    #     return
    #
    #
    # def get_incident_ray_angle(self, rayList):
    #     for ray in rayList:
    #         self.fermatManager(ray, window[0])
    #     return


