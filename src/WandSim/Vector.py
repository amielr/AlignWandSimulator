import math
import numpy as np

class Vector():
    x, y, z = 0, 0, 0

    def __init__(self, _x=None, _y=None, _z=None):

        self.x = 0 if _x is None else _x
        self.y = 0 if _y is None else _y
        self.z = 0 if _z is None else _z

    def __str__(self):
        return "The vector values are: x %s, y %s , z %s" % (self.x, self.y, self.z)

    def set_z(self,_z):
        self.z = _z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def cross_product(self, vector):
        crossX = self.y * vector.z - self.z * vector.y
        crossY = self.z * vector.x - self.x * vector.z
        crossZ = self.x * vector.y - self.y * vector.x

        return Vector(crossX, crossY, crossZ)

    def dot_product(self, vector):
        dotresult = self.x * vector.x + self.y * vector.y + self.z * vector.z
        return dotresult


    def length(self):
        lengthresult = math.sqrt(self.dot_product(self))
        return lengthresult

    def angle(self, vector):
        angleresult = math.acos(self.dot_product(vector)/(self.length()*vector.length()))
        return angleresult





