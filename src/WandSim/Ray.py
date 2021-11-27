import math
import numpy as np
from src.WandSim.Vector import *

class Ray():

    ParentSource = 'string'
    NumberOfRays = 0
    Origin = Vector(0, 0, 0)
    Direction = Vector(0, 0, 0)
    Amplitude = 1
    Wavelength = 450

    def __init__(self, _origin=None, _direction=None, _amplitude=None, _parentsource=None):

        self.Origin = Vector(0, 0, 0) if _origin is None else Vector(_origin[0], _origin[1], _origin[2])
        self.Direction = Vector(0, 0, 0) if _direction is None else Vector(_direction[0], _direction[1], _direction[2])
        self.Direction.normalize()
        self.Amplitude = 0 if _amplitude is None else _amplitude
        self.ParentSource = 'NoName' if _parentsource is None else _parentsource
        Ray.NumberOfRays += 1

    def __str__(self):
        return "The ray object values are: Origin - %s Direction - %s Amplitude - %s ParentSource - %s"\
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
        #self.Direction.normalize()
        return self.Direction

    def set_origin(self, _x, _y, _z):
        self.Origin = Vector(_x,_y,_z)


    def set_direction(self, _dx, _dy, _dz):
        self.Direction = Vector(_dx, _dy, _dz)
        self.Direction.normalize()

    def get_refraction_ratio(self, _ni, _nt):
        return _ni/_nt

    def get_ray_wavelength(self):
        return self.Wavelength

    # def snell_refraction(self, _windownormalvector, _refractiveratio):
    #
    #     transmittedRay = math.sqrt(1-math.pow(_refractiveratio, 2)*(1 - math.pow(self.get_direction().dot_product(_windownormalvector), 2)))\
    #                      * self.get_direction() + _refractiveratio*(self.get_direction() - _windownormalvector.dot_product(self.get_direction()*_windownormalvector))
    #
    #     self.set_direction(transmittedRay[0], transmittedRay[1], transmittedRay[2])
    #     return transmittedRay

    def snell_law(self, _windownormalvector, _refractivMuRatio):
        s2 = (_windownormalvector.cross_product(_windownormalvector.cross_product(self.Direction))*-1) * _refractivMuRatio\
             - _windownormalvector * math.sqrt(1-math.pow(_refractivMuRatio, 2) *
                                               _windownormalvector.cross_product(self.Direction).
                                               dot_product(_windownormalvector.cross_product(self.Direction)))

        self.set_direction(s2.x, s2.y, s2.z)
        return self


    # def propRays(ray, distance):
    #     newRay = ray
    #     newRay[0] = getOrigin(ray) + getDirection(ray) * distance
    #     return newRay
    #
    # def propogate_rays_in_free_space(rayList, distance):
    #     propogatedRays = [propRays(ray, distance) for ray in rayList]
    #     return propogatedRays

