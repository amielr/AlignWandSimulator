import json
from scipy.optimize import minimize
from src.WandSim.WindowLens import *
from src.WandSim.Projector import get_rotation_matrix
import math
from src.visuliazation.PlotFunctions import plot_xy_scatter_camera_sensor, plot_ray_path_line
from numpy import genfromtxt

with open('../src/System_Parameters/config.json') as config_file:
    config = json.load(config_file)

def get_interpolated_sensor_location_given_angle(angleInput):

    holder = np.genfromtxt('../src/System_Parameters/CameraAngleSensorRelation.csv', delimiter=',')
    Angle = holder[1::, 0]
    Sensorlocation = holder[1::, 1]
    # print(Angle)
    # print(Sensorlocation)
    print(np.interp(angleInput, Angle, Sensorlocation))
    return np.interp(angleInput, Angle, Sensorlocation)


class Camera():

    cameraName = "Camera 1"
    center = np.array([0, 0, 0])
    direction = np.array([0, 0, 0])
    rotationDirection = np.array([0, 0, 0])
    NoOfCameras = 0
    const = 1

    #Camerawindow = WindowLens()

    def __init__(self, _name, _center, _direction, _rotation, _type, _windowthickness, _refractiveindex, windowOnOff):
        self.cameraRayList = [] # is this really working???
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.cameraType = "noType" if _type is None else _type
        self.windowthickness = 0 if _windowthickness is None else _windowthickness
        self.refractiveindex = _refractiveindex if _refractiveindex is None else _refractiveindex
        print("initialising camera -        center, direction",self.center, self.direction)
        if windowOnOff == "On":
            self.window = WindowLens(self.cameraName+"window", self.windowthickness, self.center+self.windowthickness*self.direction, self.direction, self.refractiveindex)
            print("initialising camera window- center , direction", self.window.CenterPoint, self.window.Normal)


        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection)

    def add_camera_window_to_window_list(self, windowList):
        windowList.append(self.window)
        return windowList

    def ray_plane_intersection(self, ray, surface):
        DirectionVector =  self.center-ray.Origin
        DirectionVector = DirectionVector/np.linalg.norm(DirectionVector)

        lineplanetest = np.dot(surface.Normal, DirectionVector)
        epsilon = 1e-6
        if abs(lineplanetest) < epsilon:
            print("we have an intersection error: no intersection or line is within plane")
        else:
            kfactor = np.dot(surface.CenterPoint-ray.Origin, surface.Normal) / np.dot(DirectionVector, surface.Normal)

            if kfactor >= 0:
                intersectionpoint = ray.Origin + DirectionVector * kfactor
                return surface, kfactor, intersectionpoint
            else:

                print("the intersection point is behind us, ray does not meet plane-Camera", ray.Origin, surface.CenterPoint)

    def reorder_surfaces_closest_to_furthest(self, ray, surfaceList):
        kfactorList = []
        surfList = []
        intersectionList = []
        for surface in surfaceList:

            surf, kfact, intpoint = self.ray_plane_intersection(ray, surface)
            surfList.append(surf)
            kfactorList.append(kfact)
            intersectionList.append(intpoint)

        orderedList = [x for _, x in sorted(zip(kfactorList, surfaceList), reverse=False)]
        return orderedList



    def get_intersection_with_camera_no_windows(self,ray):
        ray.write_the_story(self.cameraName, self.center, 1)
        return ray


    def get_initial_intersection_points_from_surface_to_camera_v2(self, ray, windowList):

        kfactorList = []
        surfaceList = []
        intersectionList = []
        depthCounter = 1
        len(windowList)
        if len(windowList) != 0:
            windowList = self.reorder_surfaces_closest_to_furthest(ray, windowList)
        for window in windowList:
            window.surfaceList = self.reorder_surfaces_closest_to_furthest(ray, window.surfaceList)

            for surface in window.surfaceList:
                ray.IsRayInWindow = not ray.IsRayInWindow
                window.ray_window_refractive_registration(ray)

                surf, kfact, intpoint = self.ray_plane_intersection(ray, surface)

                surfaceList.append(surf)
                kfactorList.append(kfact)
                intersectionList.append(intpoint)

                depthCounter +=1
                ray.write_the_story(surf.Name, intpoint, ray.RayMuuValue)
        depthCounter += 1
        ray.write_the_story(self.cameraName, self.center, 1)

        sortedSurfacesList = [x for _, x in sorted(zip(kfactorList, surfaceList),reverse=False)]
        ray.windowSurfaceList = sortedSurfacesList
        ray.depthCounter = depthCounter
        #print(ray.RayStoryCoordinates[])
        ray.SpottoCameraRayList = ray.RayStoryCoordinates[-ray.depthCounter:]
        return ray

    def determine_time_distance_path_length(self, ray):
        distancesList = np.linalg.norm(np.diff(ray.SpottoCameraRayList, axis=0), axis=1)
        products = [a * b for a, b in zip(distancesList, ray.RayrefractiveIndexList[-ray.depthCounter:-1])]
        ray.RayPathDistance = np.sum(products)
        #print("total path distance after index correction= ", ray.RayPathDistance)
        return ray.RayPathDistance

    def slice_xy_intersect_of_surfaces_and_flatten(self, arr):
        holder = arr[1:-1]
        holder = [l[0:2] for l in holder]
        holder = [item for sublist in holder for item in sublist]
        return holder

    def replace_xyz_sliceintersects_of_surfaces(self, arr, adjusted):
        arr[1:-1] = adjusted
        return arr

    def objective_function_to_minimize_ray_path_distance(self, surfaceXYmatrix, *args):
        ray = args[0]
        #ray.DottoCameraRayList = []
        adjustedXYZList = []
        reshapedsurfaceXYmatrix = np.reshape(surfaceXYmatrix, (-1, 2))
        #plot_ray_path_line([ray])

        for index, surfaceXY in enumerate(reshapedsurfaceXYmatrix):
            z = ray.windowSurfaceList[index].determine_surface_z_given_xy(surfaceXY)
            #print("window surface name", ray.windowSurfaceList[index].Name, "xy locations are: ", surfaceXY, "z location: ", z)
            z = np.asarray(z)
            slicedList = np.append(surfaceXY, z)
            adjustedXYZList.append(slicedList)
        adjustedXYZList = np.asarray(adjustedXYZList)
        ray.SpottoCameraRayList = self.replace_xyz_sliceintersects_of_surfaces(ray.SpottoCameraRayList, adjustedXYZList)
        ray.RayStoryCoordinates[-len(ray.SpottoCameraRayList):len(ray.RayStoryCoordinates)] = ray.SpottoCameraRayList
        #print("Full ray story: ", ray.RayStoryCoordinates)
        #print("path distance is: ", self.determine_time_distance_path_length(ray))
        pathresult = self.determine_time_distance_path_length(ray)
        #plot_ray_path_line([ray])
        return pathresult

    def update_camera_rays_directions(self):
        for ray in self.cameraRayList:
            ray.Direction = (ray.RayStoryCoordinates[-1]-ray.RayStoryCoordinates[-2])/np.linalg.norm((ray.RayStoryCoordinates[-1]-ray.RayStoryCoordinates[-2]))

    def optimize_camera_rays_surface_incident_points(self):
        for ray in self.cameraRayList:
            self.determine_time_distance_path_length(ray)
            initialConditions = self.slice_xy_intersect_of_surfaces_and_flatten(ray.SpottoCameraRayList)
            initialConditions = np.asarray(initialConditions)
            boundsx = (-30, 30)
            boundsy = (-20, 20)
            bounds = [boundsx for i in range(len(initialConditions))]
            res = minimize(self.objective_function_to_minimize_ray_path_distance, initialConditions, bounds=bounds, args = (ray,))
            print("Optimization results: ", res)
            #print("our camera intersection points after are: ", ray.DottoCameraRayList)
            #print(len(ray.windowSurfaceList))#.determine_surface_z_given_xy(surfaceXY)
            #print(z)
            #print("the result is", result)
            #self.update_camera_ray_directions()
        return


    def pixelIndexing(self, XLocations, YLocations):
        holder = np.genfromtxt('../src/System_Parameters/CameraAngleSensorRelation.csv', delimiter=',')
        Sensorlocation = holder[1::, 1]
        XLocations/0.0014
        YLocations/0.0014
        Xindex = np.interp(XLocations, (-1.344, 1.344), (960, 0))
        Yindex = np.interp(YLocations, (-0.756, 0.756), (540, 0))
        Xindex = np.asarray(Xindex, dtype=float)
        Yindex = np.asarray(Yindex, dtype=float)
        print("Our pixel indexing:", Xindex, Yindex)

        return Xindex, Yindex

    def determine_pixel_locations(self):
        XanglesList = []
        YanglesList = []
        for ray in self.cameraRayList:
            directionHolder = np.matmul(np.linalg.inv(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])), ray.Direction)
            ray.Direction = np.matmul( np.linalg.inv(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])),ray.Direction)
            #print("directionholder", directionHolder)
            #ray.Direction =
            if np.dot(ray.Direction, self.direction)<0:
                xangle = math.degrees(math.asin(ray.Direction[0]/np.linalg.norm(ray.Direction)))
                yangle = math.degrees(math.asin(ray.Direction[1]/np.linalg.norm(ray.Direction)))
                XanglesList.append(xangle)
                YanglesList.append(yangle)
            else:
                xangle = math.degrees(math.asin(ray.Direction[0] / np.linalg.norm(ray.Direction)))
                yangle = math.degrees(math.asin(ray.Direction[1]/np.linalg.norm(ray.Direction)))
                XanglesList.append(xangle)
                YanglesList.append(yangle)

            #print("The angle between camera and ray is: ", self.direction,ray.Direction, angleresult, xangle, yangle)
        print("angle list", XanglesList, YanglesList)
        XLocations = get_interpolated_sensor_location_given_angle(XanglesList)
        YLocations = get_interpolated_sensor_location_given_angle(YanglesList)
        Xindexed, Yindexed = self.pixelIndexing(XLocations, YLocations)

        #testOptions = config["Validation_strings"]
        #for option in testOptions:
        my_data = genfromtxt('../src/Validation_Data/B2-CCM1.csv', delimiter=',', skip_header=1)


        Xvalidation = my_data[:, 0]
        Xvalidation -= -7.5
        Yvalidation = 540-my_data[:, 1]
        Yvalidation -= -7.5

        #print("validation data is: ", my_data)
        print("validation X data is: ", my_data[:, 0])
        print("validation Y data is: ", my_data[:, 1])

        plot_xy_scatter_camera_sensor(Xindexed, Yindexed, 0, 0)# Xvalidation, Yvalidation)
        return
