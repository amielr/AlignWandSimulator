import math
import numpy as np
from src.WandSim.Vector import *

class Ray():

    ParentSource = 'string'
    NumberOfRays = 0
    Origin = Vector()
    Direction = Vector()
    Amplitude = 1
    Wavelength = 0

    def __init__(self, _origin=None, _direction=None, _amplitude=None, _parentsource=None):

        self.Origin = (0, 0, 0) if _origin is None else _origin
        self.Direction = (0, 0, 0) if _direction is None else _direction
        self.Amplitude = 0 if _amplitude is None else _amplitude
        self.ParentSource = 'NoName' if _parentsource is None else _parentsource
        Ray.NumberOfRays += 1

    def __str__(self):
        return "The object values are: Origin - %s Direction - %s Amplitude - %s ParentSource - %s"\
               % (self.get_origin(), self.get_direction(), self.get_amplitude(), self.get_parent_source())

    def set_parent_source(self, _parentsource):
        self.ParentSource = _parentsource
        return

    def get_parent_source(self):
        return self.ParentSource

    def set_amplitude(self, _amplitude):
        self.Amplitude = _amplitude

    def get_amplitude(self):
        return self.Amplitude

    def get_number_of_rays(self):
        return self.NumberOfRays

    def get_origin(self):
        return self.Origin

    def get_direction(self):
        return self.Direction

    def set_origin(self, _x, _y, _z):
        self.Origin = Vector(_x,_y,_z)


    def set_direction(self, _dx, _dy, _dz):
        self.Direction = Vector(_dx, _dy, _dz)

    def get_refraction_ratio(self, _ni, _nt):
        return _ni/_nt

    def snell_refraction(self, _incidentray, _windownormalvector, _refractiveratio):
        transmittedRay = math.sqrt(1-math.pow(_refractiveratio,2)*(1-math.pow(_incidentray.get_direction.dot_product(_windownormalvector), 2)))\
                            *_incidentray.get_direction + _refractiveratio*(_incidentray.get_direction- _windownormalvector.dot_product(_incidentray.get_direction)*_windownormalvector)


        return transmittedRay

    def transmit_ray_through_window(self, _windowobject):

        return

    # def propRays(ray, distance):
    #     newRay = ray
    #     newRay[0] = getOrigin(ray) + getDirection(ray) * distance
    #     return newRay
    #
    # def propogate_rays_in_free_space(rayList, distance):
    #     propogatedRays = [propRays(ray, distance) for ray in rayList]
    #     return propogatedRays

