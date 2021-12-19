from src.WandSim.Vector import *

class Ray():

    ParentSource = 'string'
    EventRegister = 'string'
    NumberOfRays = 0
    Origin = np.array([0, 0, 0])
    Direction = np.array([0, 0, 0])
    Amplitude = 1
    Wavelength = 450

    def __init__(self, _origin=None, _direction=None, _amplitude=None, _parentsource=None):

        self.Origin = np.array([0, 0, 0]) if _origin is None else np.array([_origin[0], _origin[1], _origin[2]])
        self.Direction = np.array([0, 0, 0]) if _direction is None else np.array([_direction[0], _direction[1], _direction[2]])
        self.Direction = self.normalize(self.Direction)
        self.Amplitude = 0 if _amplitude is None else _amplitude
        self.ParentSource = 'NoName' if _parentsource is None else _parentsource
        self.EventRegister = 'NoName' if _parentsource is None else _parentsource
        Ray.NumberOfRays += 1

    def __str__(self):
        return "Ray values: Origin - %s Direction - %s Amplitude - %s ParentSource - %s"\
               % (self.get_origin(), self.get_direction(), self.get_amplitude(), self.get_parent_source())

    def normalize(self, an_array):
        norm = np.linalg.norm(an_array)
        normal_array = an_array / norm
        return normal_array

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
        self.Origin = np.array([_x, _y, _z])

    def set_direction(self, _dx, _dy, _dz):
        self.Direction = np.array([_dx, _dy, _dz])
        self.Direction = self.normalize(self.Direction)

    def get_ray_wavelength(self):
        return self.Wavelength

    def snell_law_v2(self, _windownormalvector, _refractivmuratio):
        s2 = _windownormalvector*math.sqrt(1-math.pow(_refractivmuratio, 2)*(1-math.pow(np.dot(_windownormalvector, self.Direction), 2)))\
             + (self.Direction - _windownormalvector*(np.dot(_windownormalvector, self.Direction)))*_refractivmuratio

        self.set_direction(s2[0], s2[1], s2[2])

    def ray_surface_intersection(self, _surface, epsilon=1e-6):

        surfacenormal = _surface.get_surface_normal()
        rayorigin = self.get_origin()
        raydirection = self.get_direction()
        originplanepointvector = _surface.CenterPoint - rayorigin

        lineplanetest =  np.dot(surfacenormal, raydirection)

        if abs(lineplanetest) < epsilon:
            print("we have an intersection error: no intersection or line is within plane")
        else:
            kfactor = np.dot(originplanepointvector, surfacenormal) / np.dot(raydirection, surfacenormal)

            if kfactor >= 0:
                intersectionpoint = rayorigin + raydirection * kfactor
                self.set_origin(intersectionpoint[0], intersectionpoint[1], intersectionpoint[2])
                # print("The intersection point is: %s" % (self.get_origin()))
            else:
                print("the intersection point is behind us, ray does not meet plane")

    def get_reflection_from_surface(self, _surface):
        surfacenormal = _surface.get_surface_normal()
        ndot = np.dot(self.Direction, surfacenormal)
        reflectedRayDirection = self.Direction - surfacenormal * (2 * ndot)

        return self.set_direction(reflectedRayDirection[0], reflectedRayDirection[1], reflectedRayDirection[2])

    def register_event(self,_objectname):
        self.EventRegister += str(_objectname)
        return
    # def propRays(self, distance):
    #     newRay = self
    #     newRay[0] = getOrigin(ray) + getDirection(ray)*distance
    #     return newRay
    #
    # def propogate_rays_in_free_space(self, distance):
    #     propogatedRays = [propRays(ray, distance) for ray in rayList]
    #     return propogatedRays