from src.WandSim.Surface import Surface
from src.WandSim.Ray import Ray
import numpy as np


class WindowLens:
    RefractiveIndexDictionary = 0
    Thickness = 0
    MuIn = 0
    MuOut = 0
    s1surface = Surface
    s2surface = Surface
    CenterPoint = np.array([0, 0, 0])
    Normal = np.array([0, 0, 0])
    Name = 'string'

    def __init__(self, _windowname=None, _thickness=None, _centralpoint=None, _normal=None, _refractiveindex=None):
        self.Name = "noName" if _windowname is None else _windowname
        self.CenterPoint = np.array([0, 0, 0]) if _centralpoint is None else _centralpoint
        self.Normal = np.array([0, 0, 1]) if _normal is None else _normal
        self.Thickness = 0 if _thickness is None else _thickness
        self.s1surface = Surface((_windowname + "S1"), _centralpoint, _normal)
        self.s2surface = self.create_window_surfaces()
        self.create_surface_List()
        self.RefractiveIndexDictionary = 0 if _refractiveindex is None else _refractiveindex
        return

    def __str__(self):
        return "The Window values are: WindowName - %s Thickness - %s  RefractiveIndex - %s" \
               % (Surface.Name, self.Thickness, self.RefractiveIndexDictionary)

    def create_surface_List(self):
        self.surfaceList = []
        self.surfaceList.append(self.s1surface)
        self.surfaceList.append(self.s2surface)
        return

    def create_window_surfaces(self):
        windowS2Point = self.CenterPoint + self.Normal * self.Thickness
        surface = Surface(self.Name + "s2", windowS2Point, self.Normal)
        return surface

    def calculate_mu(self, raymu):
        self.MuIn = 1 / raymu
        self.MuOut = raymu / 1
        return

    def get_mu_in(self):
        return self.MuIn

    def get_mu_out(self):
        return self.MuOut

    def refract_ray_at_window_surface(self, _incidentray):

        if not (_incidentray.IsRayInWindow):
            _incidentray.snell_law_v2(self.Normal, self.get_mu_in())
        else:
            _incidentray.snell_law_v2(self.Normal, self.get_mu_out())
        _incidentray.IsRayInWindow = not _incidentray.IsRayInWindow

    def ray_window_refractive_registration(self, _incidentray):
        raymuu = self.RefractiveIndexDictionary.get(str(_incidentray.get_ray_wavelength()))
        self.calculate_mu(raymuu)
        if not (_incidentray.IsRayInWindow):
            _incidentray.RayMuuValue = raymuu
        else:
            _incidentray.RayMuuValue = 1




    def propogate_ray_to_endof_window(self, _incidentray):
        surface = self.surfaceList[1]
        _incidentray.ray_surface_intersection(surface)




    def transmit_ray_through_window(self, _incidentray):
        self.ray_window_refractive_registration(_incidentray)
        self.refract_ray_at_window_surface(_incidentray)
        # print("after s1 incidence", _incidentray)
        self.propogate_ray_to_endof_window(_incidentray)
        # _incidentray.tell_the_story(self.SurfaceName, _incidentray.Origin)
        # print("at s2 incidence", _incidentray)
        self.ray_window_refractive_registration(_incidentray)
        self.refract_ray_at_window_surface(_incidentray)
        # print("after s2 transmittance", _incidentray)
        return _incidentray

    def get_surface_normal(self):
        return self.Normal
