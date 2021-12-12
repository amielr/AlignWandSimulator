from src.WandSim.Vector import *

class Ray():

    ParentSource = 'string'
    EventRegister = 'string'
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
        self.EventRegister = 'NoName' if _parentsource is None else _parentsource
        Ray.NumberOfRays += 1

    def __str__(self):
        return "Ray values: Origin - %s Direction - %s Amplitude - %s ParentSource - %s"\
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
        self.Origin = Vector(_x, _y, _z)

    def set_direction(self, _dx, _dy, _dz):
        self.Direction = Vector(_dx, _dy, _dz)
        self.Direction.normalize()

    def get_ray_wavelength(self):
        return self.Wavelength

    # def snell_law(self, _windownormalvector, _refractivmuratio):
    #     s2 = (_windownormalvector.cross_product((_windownormalvector*(-1)).cross_product(self.Direction))) * \
    #          _refractivmuratio - _windownormalvector * (math.sqrt(1 - math.pow(_refractivmuratio, 2) *
    #                                            _windownormalvector.cross_product(self.Direction).
    #                                            dot_product(_windownormalvector.cross_product(self.Direction))))
    #
    #     self.set_direction(s2.x, s2.y, s2.z)
    #     return self

    def snell_law_v2(self, _windownormalvector, _refractivmuratio):
        s2 = _windownormalvector*math.sqrt(1-math.pow(_refractivmuratio, 2)*(1-math.pow(_windownormalvector.dot_product(self.Direction), 2)))\
             + (self.Direction - _windownormalvector*(_windownormalvector.dot_product(self.Direction)))*_refractivmuratio

        self.set_direction(s2.x, s2.y, s2.z)


    def ray_surface_intersection(self, _surface, epsilon=1e-6):

        surfacenormal = _surface.get_surface_normal()
        rayorigin = self.get_origin()
        raydirection = self.get_direction()
        originplanepointvector = _surface.CenterPoint - rayorigin

        lineplanetest = surfacenormal.dot_product(raydirection)

        if abs(lineplanetest) < epsilon:
            print("we have an intersection error: no intersection or line is within plane")
        else:
            kfactor = originplanepointvector.dot_product(surfacenormal) / raydirection.dot_product(surfacenormal)

            if kfactor >= 0:
                intersectionpoint = rayorigin + raydirection * kfactor
                self.set_origin(intersectionpoint.x, intersectionpoint.y, intersectionpoint.z)
                # print("The intersection point is: %s" % (self.get_origin()))
            else:
                print("the intersection point is behind us, ray does not meet plane")

    def get_reflection_from_surface(self, _surface):
        surfacenormal = _surface.get_surface_normal()
        ndot = self.Direction.dot_product(surfacenormal)
        reflectedRayDirection = self.Direction - surfacenormal * (2 * ndot)

        return self.set_direction(reflectedRayDirection.x, reflectedRayDirection.y, reflectedRayDirection.z)

    def register_event(self,_objectname):
        self.EventRegister += str(_objectname)
        return
