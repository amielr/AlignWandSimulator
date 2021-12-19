import math
import numpy as np

origin = np.array([0, 0, 0], dtype=np.float_)

class Vector():
    x, y, z = 0, 0, 0

    def __init__(self, _x=None, _y=None, _z=None):

        self.x = 0 if _x is None else _x
        self.y = 0 if _y is None else _y
        self.z = 0 if _z is None else _z

    def __str__(self):
        return "Vector: x %s, y %s , z %s" % (self.x, self.y, self.z)

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

    def normalize(self):
        normalizer = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
        length = self.length()
        self.x = self.x/normalizer
        self.y = self.y/normalizer
        self.z = self.z/normalizer
        return

    #def __sub__(self, vector):
    #    return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

    def __add__(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
