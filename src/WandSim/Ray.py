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

    def __init__(self, _origin=Vector(0, 0, 0), _direction=Vector(0, 0, 0), _amplitude=0, _parentsource ='random'):
        self.Origin = _origin

        self.Direction = _direction

        self.set_amplitude(_amplitude)

        self.set_parent_source(_parentsource)

        Ray.NumberOfRays += 1

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
        self.Origin = Vector(_x, _y, _z)

    def set_direction(self, _dx, _dy, _dz):
        self.Direction = Vector(_dx, _dy, _dz)