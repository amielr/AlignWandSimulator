from copy import deepcopy
import json
import numpy as np
from scipy.optimize import minimize
from src.WandSim.WindowLens import *


#import cupy as np

with open('../src/config.json') as config_file:
    config = json.load(config_file)


class Camera():

    cameraName = "Camera 1"
    center = np.array([0, 0, 0])
    direction = np.array([0, 0, 0])
    rotationDirection = np.array([0, 0, 0])
    NoOfCameras = 0
    const = 1
    #Camerawindow = WindowLens()

    def __init__(self, _name, _center, _direction, _rotation, _type, _windowthickness, _refractiveindex):
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        #self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.cameraType = "noType" if _type is None else _type
        self.windowthickness = 0 if _windowthickness is None else _windowthickness
        self.refractiveindex = _refractiveindex if _refractiveindex is None else _refractiveindex
        self.window = WindowLens(self.cameraName+"window", self.windowthickness, self.center+self.direction, self.direction, self.refractiveindex)

        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection)


    def setupwindowlens(self):
        WindowLens(self.cameraName+"window", 0.2, self.center+self.const*self.direction, self.direction, 1.5)


    def reorder_list_from_closest_to_furthest(self, ray, surfaceList):
        distanceList = []
        flag = False
        for surface in surfaceList:
            distance = np.linalg.norm(ray.Origin - surface.CenterPoint)
            distanceList.append(distance)
            print(str(surface.Name) + " distance from ray origin to surface camera module: " + str(distance))

        sortedSurfacesList = [x for _, x in sorted(zip(distanceList, surfaceList))]
        #[print(surfaceholder.CenterPoint) for surfaceholder in sortedSurfacesList]
        return sortedSurfacesList

    def camera_windows_transfer_manager(self, window, ray):
        ray.ray_surface_intersection(window.surfaceList[0])
        ray.DottoCameraRayList.append(ray.Origin)
        ray.IsRayInWindow = not ray.IsRayInWindow
        window.ray_window_refractive_registration(ray)
        ray.ray_surface_intersection(window.surfaceList[1])
        ray.DottoCameraRayList.append(ray.Origin)
        return

    def add_camera_window_to_window_list(self, windowList):
        windowList.append(self.window)
        return windowList

    def get_initial_intersection_points_from_surface_to_camera(self, rayList, windowsList):

        # self.windowListholder = deepcopy(windowsList)
        # self.add_camera_window_to_window_list(windowsList)
        # self.add_camera_window_to_window_list(self.windowListholder)
        # print(windowsList)
        # print("camera window list", self.windowListholder)



        self.cameraRayList = deepcopy(rayList)
        #print("we are here", self.cameraRayList)
        for ray in self.cameraRayList:
            ray.Direction = ray.normalize(self.center - ray.Origin)
            sortedwindowsList = self.reorder_list_from_closest_to_furthest(ray, windowsList)
            ray.DottoCameraRayList = [ray.Origin]
            ray.windowSurfaceList =[]
            for window in sortedwindowsList:
                window.surfaceList = self.reorder_list_from_closest_to_furthest(ray, window.surfaceList)
                ray.windowSurfaceList.append(window.surfaceList)
                ray.IsRayInWindow = not ray.IsRayInWindow
                window.ray_window_refractive_registration(ray)
                self.camera_windows_transfer_manager(window, ray)
                #print(self.cameraName, " ray surface intersection", ray.Origin)
            #print("window surface list length: ", str(len(ray.windowSurfaceList)))
            ray.set_origin(self.center)

            ray.DottoCameraRayList.append(ray.Origin)
            ray.DottoCameraRayList = np.asarray(ray.DottoCameraRayList)

            ray.write_the_story(self.cameraName, ray.Origin, ray.RayMuuValue)
            ray.windowSurfaceList = [item for sublist in ray.windowSurfaceList for item in sublist]

        return self.cameraRayList

    def determine_time_distance_path_length(self, ray):
        distance = 0
        #print("ray to be determined", ray)
        distancesList = np.linalg.norm(np.diff(ray.RayStoryCoordinates, axis=0), axis=1)
        #print("distance list: ", distancesList)
        #ray.RayrefractiveIndexList = np.delete(ray.RayrefractiveIndexList, 0)
        #print("refractive index list = ", ray.RayrefractiveIndexList)
        ray.RayPathDistance = np.sum(distancesList)
        #print(ray.RayStory)
        #print(ray.RayStoryCoordinates)
        #print("total path distance before index correction = ", ray.RayPathDistance)
        #print(list(zip(distancesList, ray.RayrefractiveIndexList)))
        products = [a * b for a, b in zip(distancesList, ray.RayrefractiveIndexList)]
        ray.RayPathDistance = np.sum(products)
        #print("total path distance after index correction= ", ray.RayPathDistance)
        return ray.RayPathDistance


    def slice_XY_intersect_of_Surfaces(self, arr):
        return arr[1:-1, 0:2]

    def replace_XYZ_sliceintersects_of_Surfaces(self, arr, adjusted):
        arr[1:-1, 0:3] = adjusted
        return arr

    def objective_function_to_minimize_ray_path_distance(self, surfaceXYmatrix, *args):
        ray = args[0]
        adjustedXYZList = []
        reshapedsurfaceXYmatrix = np.reshape(surfaceXYmatrix, (-1, 2))
        for index, surfaceXY in enumerate(reshapedsurfaceXYmatrix):
            # surfaceXY = [10,10]
            z = ray.windowSurfaceList[index].determine_surface_z_given_xy(surfaceXY)
            #print("xy locations are: ", surfaceXY, "z location: ", z)
            z = np.asarray(z)
            slicedList = np.append(surfaceXY, z)
            adjustedXYZList.append(slicedList)

            #print(slicedList)
        adjustedXYZList = np.asarray(adjustedXYZList)
        #print(adjustedXYZList)
        ray.DottoCameraRayList = self.replace_XYZ_sliceintersects_of_Surfaces(ray.DottoCameraRayList, adjustedXYZList)
        #print(ray.DottoCameraRayList)
        ray.RayStoryCoordinates[-len(ray.DottoCameraRayList):len(ray.RayStoryCoordinates), :] = ray.DottoCameraRayList
        #print("Full ray story: ", ray.RayStoryCoordinates)
        # surfaceXY[index] =
        pathresult = self.determine_time_distance_path_length(ray)
        return pathresult



    def optimize_Camera_rays(self):
        for ray in self.cameraRayList:
            self.determine_time_distance_path_length(ray)

            #print("our camera intersection points are: ", ray.DottoCameraRayList)

            #print("sliced: ", self.slice_XY_intersect_of_Surfaces(ray.DottoCameraRayList))
            #[[5,7],[10,10],[11,11],[1,1]]
            initialConditions = self.slice_XY_intersect_of_Surfaces(ray.DottoCameraRayList).flatten()
            #print(type(initialConditions))
            self.objective_function_to_minimize_ray_path_distance(initialConditions, ray)
            boundsx = (-20, 20)
            boundsy = (-20, 20)
            bounds = [boundsx for i in range(len(initialConditions))]
            #print("function type is: ", type(self.objective_function_to_minimize_ray_path_distance), type(ray))
            result = minimize(self.objective_function_to_minimize_ray_path_distance, initialConditions, bounds=bounds, args = (ray,))
                #print(len(ray.windowSurfaceList))#.determine_surface_z_given_xy(surfaceXY)
                #print(z)
            #print("the result is", result)

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


