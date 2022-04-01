#from src.WandSim.WindowLens import *
import numpy as np
import math
import csv


class Ray():

    ParentSource = ''
    RayStory = ''
    NumberOfRays = 0
    #Origin = np.empty((1, 3))
    #Direction = np.empty((1, 3))
    Amplitude = 1
    IndexI = 0
    IndexJ = 0
    Wavelength = 450
    IsRayInWindow = False
    RayMuuValue = 1
    RayPathDistance = 0
    RayStoryCoordinates = np.array(0)

    def __init__(self, _origin=None, _direction=None, _amplitude=None, _parentsource=None, _Iindex = None, _Jindex = None):

        self.Origin = np.array([0, 0, 0]) if _origin is None else np.array([_origin[0], _origin[1], _origin[2]])
        self.Direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.Direction = self.normalize(self.Direction)
        self.Amplitude = 0 if _amplitude is None else _amplitude
        self.ParentSource = 'NoName' if _parentsource is None else _parentsource
        self.EventRegister = 'NoName' if _parentsource is None else _parentsource
        self.IndexI = _Iindex
        self.IndexJ = _Jindex
        self.write_the_story(_parentsource.projectorName, self.Origin, 1)
        Ray.NumberOfRays += 1

    def __str__(self):
        return "Ray values: Origin - %s Direction - %s Amplitude - %s ParentSource - %s"\
               % (self.Origin, self.Direction, self.get_amplitude(), self.get_parent_source())

    def normalize(self, an_array):
        norm = np.linalg.norm(an_array)
        normal_array = an_array / norm
        return normal_array


    def get_parent_source(self):
        return self.ParentSource

    def set_amplitude(self, _amplitude):
        self.Amplitude = _amplitude

    def get_amplitude(self):
        return self.Amplitude

    def get_number_of_rays(self):
        return self.NumberOfRays


    def set_origin(self, _origin):
        self.Origin = _origin

    def set_direction(self, _direction):
        self.Direction = _direction
        self.Direction = self.normalize(self.Direction)

    def get_ray_wavelength(self):
        return self.Wavelength

    def snell_law_v2(self, _windownormalvector, _refractivmuratio):
        #print(self.Direction)
        index = 1-math.pow(_refractivmuratio, 2)*(1 - math.pow(np.dot(_windownormalvector, self.Direction), 2))
        if (index) < 0:
            print("total internal reflection", index)
        else:
            s2 = math.sqrt(1-math.pow(_refractivmuratio, 2)*(1-math.pow(np.dot(_windownormalvector, self.Direction), 2)))*_windownormalvector\
                 + _refractivmuratio*(self.Direction - (np.dot(_windownormalvector, self.Direction))*_windownormalvector)
            self.set_direction(np.array([s2[0], s2[1], s2[2]]))


    def ray_surface_intersection(self, _surface, epsilon=1e-6):

        #print(isinstance(_surface, WindowLens))
        surfacenormal = _surface.get_surface_normal()
        rayorigin = self.Origin
        raydirection = self.Direction
        originplanepointvector = _surface.CenterPoint - rayorigin

        lineplanetest = np.dot(surfacenormal, raydirection)

        if abs(lineplanetest) < epsilon:
            print("we have an intersection error: no intersection or line is within plane")
        else:
            kfactor = np.dot(originplanepointvector, surfacenormal) / np.dot(raydirection, surfacenormal)

            if kfactor >= 0:
                intersectionpoint = rayorigin + raydirection * kfactor
                #fixing
                self.set_origin(intersectionpoint)
                self.write_the_story(_surface.Name, self.Origin, self.RayMuuValue)
                # print("The intersection point is: %s" % (self.get_origin()))
                return(self.Origin)
            else:

                print("the intersection point is behind us, ray does not meet plane", self.Origin, _surface.CenterPoint)


    def get_reflection_from_surface(self, _surface):
        surfacenormal = _surface.get_surface_normal()
        ndot = np.dot(self.Direction, surfacenormal)
        reflectedRayDirection = self.Direction - surfacenormal * (2 * ndot)
        self.set_direction(reflectedRayDirection)

        #self.write_the_story(_surface.Name, self.Origin, self.RayMuuValue)
        return

    def write_the_story(self, _objectname, coordinates, refractiveIndex):
        if len(self.RayStory) == 0:
            self.RayStory += str(_objectname + ",")
            self.RayrefractiveIndexList = np.array(refractiveIndex)
            self.RayStoryCoordinates = coordinates
        else:
            self.RayStory += str(_objectname + ",")
            self.RayrefractiveIndexList = np.hstack((self.RayrefractiveIndexList, self.RayMuuValue))
            self.RayStoryCoordinates = np.vstack((self.RayStoryCoordinates, coordinates))

        return

    def tell_the_story(self):
        print(self.RayStoryCoordinates)
        print(self.RayStory)
        print(self.RayrefractiveIndexList)

    def print_the_story(self):
        with open('output.csv', 'w') as result_file:
            wr = csv.writer(result_file, dialect='excel')
            wr.writerow(self.RayStory)
            wr.writerow('/n')

