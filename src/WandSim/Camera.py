from copy import deepcopy
import json
from scipy.optimize import minimize
from src.WandSim.WindowLens import *
from src.WandSim.Projector import get_rotation_matrix
import math
from src.visuliazation.PlotFunctions import plot_xy_scatter, plot_ray_path_line



with open('../src/System_Parameters/config.json') as config_file:
    config = json.load(config_file)

def get_interpolated_sensor_location_given_angle(angleInput):
    # with open('../src/System_Parameters/CameraAngleSensorRelation.csv', newline='') as csvfile:
    #     AngleSensorRelation = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in AngleSensorRelation:
    #         print(', '.join(row))

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

    def __init__(self, _name, _center, _direction, _rotation, _type, _windowthickness, _refractiveindex):
        self.cameraName = "noName" if _name is None else _name
        self.center = np.array([0, 0, 0]) if _center is None else np.array([_center[0], _center[1], _center[2]])
        self.direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.rotationDirection = np.array([0, 0, 0]) if _rotation is None else np.array([_rotation[0], _rotation[1], _rotation[2]])
        self.direction = np.matmul(get_rotation_matrix(_rotation[0], _rotation[1], _rotation[2]), self.direction)
        self.cameraType = "noType" if _type is None else _type
        self.windowthickness = 0 if _windowthickness is None else _windowthickness
        self.refractiveindex = _refractiveindex if _refractiveindex is None else _refractiveindex
        print("initialising camera -        center, direction",self.center, self.direction)
        self.window = WindowLens(self.cameraName+"window", self.windowthickness, self.center+self.windowthickness*self.direction, self.direction, self.refractiveindex)
        print("initialising camera window- center , direction",self.window.CenterPoint, self.window.Normal)

        return

    def __str__(self):
        return "Camera Name: %s - Origin %s, - Direction  %s, - Rotation %s "\
               % (self.cameraName, self.center, self.direction, self.rotationDirection)


    def reorder_list_from_closest_to_furthest(self, ray, surfaceList):
        distanceList = []
        flag = False
        for surface in surfaceList:
            distance = np.linalg.norm(ray.Origin - surface.CenterPoint)
            distanceList.append(distance)
            print("ray.origin relative to surface is: ", ray.Origin, surface.CenterPoint)
            print(str(surface.Name) + " distance from ray origin to surface camera module: " + str(distance))

        sortedSurfacesList = [x for _, x in sorted(zip(distanceList, surfaceList))]
        [print(surface.Name, surface.CenterPoint) for surface in sortedSurfacesList]
        print("window order from surface to camera: ", [surfaceholder.Name for surfaceholder in sortedSurfacesList])
        print("sorted window list:", len(sortedSurfacesList))
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
                # fixing
                #self.set_origin(intersectionpoint)
                #self.write_the_story(_surface.Name, self.Origin, self.RayMuuValue)
                # print("The intersection point is: %s" % (self.get_origin()))
                return (surface, kfactor, intersectionpoint)
            else:

                print("the intersection point is behind us, ray does not meet plane-Camera", ray.Origin, surface.CenterPoint)




    def reorder_surfaces_closest_to_furthest(self,ray,surfaceList):
        kfactorList = []
        surfList = []
        intersectionList = []
        for surface in surfaceList:

            surf, kfact, intpoint = self.ray_plane_intersection(ray, surface)
            surfList.append(surf)
            kfactorList.append(kfact)
            intersectionList.append(intpoint)

        orderedList = [x for _, x in sorted(zip(kfactorList, surfaceList),reverse=False)]
        return orderedList


    def get_initial_intersection_points_from_surface_to_camera_v2(self, ray, windowList):

        kfactorList = []
        surfaceList = []
        intersectionList = []
        depthCounter = 1

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
        # sortedintersectionList = [x for _, x in sorted(zip(kfactorList, intersectionList), reverse=False)]
        # sortedintersectionList.insert(0, ray.Origin)
        # sortedintersectionList.append(self.center)
        #ray.RayStoryCoordinates = np.append(ray.RayStoryCoordinates, sortedintersectionList)
        ray.windowSurfaceList = sortedSurfacesList
        # print("sorted surface list:", sortedSurfacesList)
        # print("sorted intersection list: ", np.asarray([l.tolist() for l in sortedintersectionList]))
        #ray.DottoCameraRayList = np.asarray([l.tolist() for l in sortedintersectionList])
        #ray.RayStoryCoordinates = np.append(ray.RayStoryCoordinates, ray.DottoCameraRayList, 0)
        #print("depthcounter", depthCounter)
        ray.depthCounter = depthCounter
        #print(ray.RayStoryCoordinates[])
        ray.DottoCameraRayList = ray.RayStoryCoordinates[-ray.depthCounter:]
        return ray




    # def get_initial_intersection_points_from_surface_to_camera(self, rayList, windowsList):
    #
    #     self.cameraRayList = deepcopy(rayList)
    #     #print("we are here", self.cameraRayList)
    #     for ray in self.cameraRayList:
    #         ray.Direction = ray.normalize(self.center - ray.Origin)
    #         sortedwindowsList = self.reorder_list_from_closest_to_furthest(ray, windowsList)
    #         print("our sorted windowslist is: ", sortedwindowsList)
    #         print("our ray Origin in Camera ray list is:", ray.Origin, ray.Direction)
    #         ray.DottoCameraRayList = [ray.Origin]
    #         print(ray.DottoCameraRayList)
    #         ray.windowSurfaceList =[]
    #
    #         for window in sortedwindowsList:
    #             window.surfaceList = self.reorder_list_from_closest_to_furthest(ray, window.surfaceList)
    #             print("window surface list", window.surfaceList)
    #             ray.windowSurfaceList.extend(window.surfaceList)
    #             print("ray surface list", len(ray.windowSurfaceList), ray.windowSurfaceList)
    #             [print(surface.Name, surface.CenterPoint) for surface in ray.windowSurfaceList]
    #
    #
    #
    #             ray.IsRayInWindow = not ray.IsRayInWindow
    #             window.ray_window_refractive_registration(ray)
    #             self.camera_windows_transfer_manager(window, ray)
    #         print("our ray surface list:", len(ray.windowSurfaceList))
    #         # print(self.cameraName, " ray surface intersection", ray.Origin)
    #         # print(self.cameraName, "ray surfaces intersection points", ray.DottoCameraRayList)
    #         # print("window surface list length: ", str(len(ray.windowSurfaceList)))
    #         ray.set_origin(self.center)
    #
    #         ray.DottoCameraRayList.append(ray.Origin)
    #         ray.DottoCameraRayList = np.asarray(ray.DottoCameraRayList)
    #         print("initial dot to camera is :", ray.DottoCameraRayList)
    #
    #
    #         ray.write_the_story(self.cameraName, ray.Origin, ray.RayMuuValue)
    #         #ray.windowSurfaceList = [item for sublist in ray.windowSurfaceList for item in sublist]
    #         [print(surface) for surface in ray.windowSurfaceList]
    #         print("ray surface list flattened", len(ray.windowSurfaceList), ray.windowSurfaceList)
    #     #plot_ray_path_line(self.cameraRayList)
    #     return self.cameraRayList

    def determine_time_distance_path_length(self, ray):
        distance = 0
        #print("ray to be determined", ray)
        distancesList = np.linalg.norm(np.diff(ray.DottoCameraRayList, axis=0), axis=1)
        #print("distance list: ", distancesList)
        #ray.RayrefractiveIndexList = np.delete(ray.RayrefractiveIndexList, 0)
        #print("refractive index list = ", ray.RayrefractiveIndexList)
        #ray.RayPathDistance = np.sum(distancesList)
        #print(ray.RayStory)
        #print(ray.RayStoryCoordinates)
        #print("total path distance before index correction = ", ray.RayPathDistance)
        #print(list(zip(distancesList, ray.RayrefractiveIndexList)))
        products = [a * b for a, b in zip(distancesList, ray.RayrefractiveIndexList[-ray.depthCounter:-1])]
        ray.RayPathDistance = np.sum(products)
        #print("total path distance after index correction= ", ray.RayPathDistance)
        return ray.RayPathDistance


    def slice_XY_intersect_of_Surfaces_and_flatten(self, arr):
        holder = arr[1:-1]
        holder = [l[0:2] for l in holder]
        holder = [item for sublist in holder for item in sublist]
        return holder

    def replace_XYZ_sliceintersects_of_Surfaces(self, arr, adjusted):
        arr[1:-1] = adjusted
        return arr

    def objective_function_to_minimize_ray_path_distance(self, surfaceXYmatrix, *args):
        ray = args[0]
        #ray.DottoCameraRayList = []
        adjustedXYZList = []
        reshapedsurfaceXYmatrix = np.reshape(surfaceXYmatrix, (-1, 2))
        #print("reshapedXYmatrix", reshapedsurfaceXYmatrix)
        #print("window surface length is:", len(ray.windowSurfaceList))
        #plot_ray_path_line([ray])

        for index, surfaceXY in enumerate(reshapedsurfaceXYmatrix):
            # surfaceXY = [10,10]

            z = ray.windowSurfaceList[index].determine_surface_z_given_xy(surfaceXY)
            #print("window surface name", ray.windowSurfaceList[index].Name, "xy locations are: ", surfaceXY, "z location: ", z)
            z = np.asarray(z)
            slicedList = np.append(surfaceXY, z)
            adjustedXYZList.append(slicedList)

            #print(slicedList)
        adjustedXYZList = np.asarray(adjustedXYZList)
        #print(adjustedXYZList)
        ray.DottoCameraRayList = self.replace_XYZ_sliceintersects_of_Surfaces(ray.DottoCameraRayList, adjustedXYZList)
        #print(ray.DottoCameraRayList)
        ray.RayStoryCoordinates[-len(ray.DottoCameraRayList):len(ray.RayStoryCoordinates)] = ray.DottoCameraRayList
        #print("Full ray story: ", ray.RayStoryCoordinates)
        # surfaceXY[index] =
        #print("path distance is: ", self.determine_time_distance_path_length(ray))
        pathresult = self.determine_time_distance_path_length(ray)
        #plot_ray_path_line([ray])

        return pathresult



    def update_camera_ray_directions(self):
        for ray in self.cameraRayList:
            ray.Direction = (ray.RayStoryCoordinates[-1]-ray.RayStoryCoordinates[-2])/np.linalg.norm((ray.RayStoryCoordinates[-1]-ray.RayStoryCoordinates[-2]))


    def optimize_Camera_rays(self):
        for ray in self.cameraRayList:
            self.determine_time_distance_path_length(ray)
            #print("our camera intersection points before are: ", ray.DottoCameraRayList)

            #print("sliced: ", self.slice_XY_intersect_of_Surfaces(ray.DottoCameraRayList))
            #[[5,7],[10,10],[11,11],[1,1]]
            #print(self.slice_XY_intersect_of_Surfaces(ray.DottoCameraRayList))
            initialConditions = self.slice_XY_intersect_of_Surfaces_and_flatten(ray.DottoCameraRayList)
            print("flattened", initialConditions)
            print("Original", self.slice_XY_intersect_of_Surfaces_and_flatten(ray.DottoCameraRayList))
            #self.objective_function_to_minimize_ray_path_distance(initialConditions, ray)
            boundsx = (-30, 30)
            boundsy = (-20, 20)
            bounds = [boundsx for i in range(len(initialConditions))]
            #print("function type is: ", type(self.objective_function_to_minimize_ray_path_distance), type(ray))
            res = minimize(self.objective_function_to_minimize_ray_path_distance, initialConditions, bounds=bounds, args = (ray,))
            #print("Optimization results: ", res)
            #print("our camera intersection points after are: ", ray.DottoCameraRayList)

                #print(len(ray.windowSurfaceList))#.determine_surface_z_given_xy(surfaceXY)
                #print(z)
            #print("the result is", result)
            self.update_camera_ray_directions()
        return

    def pixelIndexing(self, XLocations, YLocations):
        holder = np.genfromtxt('../src/System_Parameters/CameraAngleSensorRelation.csv', delimiter=',')
        Sensorlocation = holder[1::, 1]
        XLocations/0.0014
        YLocations/0.0014
        Xindex = np.interp(XLocations, (-1.344, 1.344), (-1, 1921))
        Yindex = np.interp(YLocations, (-0.756, 0.756), (-1, 1081))
        Xindex = np.asarray(Xindex, dtype=float)
        Yindex = np.asarray(Yindex, dtype=float)
        print("Our pixel indexing:", Xindex, Yindex)

        return Xindex, Yindex

    def determine_pixel_locations(self):
        XanglesList = []
        YanglesList = []
        for ray in self.cameraRayList:
            directionHolder = np.matmul(np.linalg.inv(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])), ray.Direction)
            ray.Direction = np.matmul( ray.Direction,np.linalg.inv(get_rotation_matrix(self.rotationDirection[0], self.rotationDirection[1], self.rotationDirection[2])),)
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
        plot_xy_scatter(Xindexed, Yindexed)


        return