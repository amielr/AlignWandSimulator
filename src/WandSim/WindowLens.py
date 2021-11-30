from src.WandSim.Vector import Vector
from src.WandSim.Surface import Surface
from src.WandSim.Ray import Ray


class WindowLens(Surface):

    #todo change refractive index to dictionary for different wavelengths
    RefractiveIndexDictionary = 0
    Thickness = 0
    MuIn = 0
    MuOut = 0
    IsRayInWindow = False

    def __init__(self, _windowname=None, _thickness=None, _centralpoint=None, _normal=None, _refractiveindex=None):

        super().__init__(_windowname, _centralpoint, _normal)
        self.Thickness = 0 if _thickness is None else _thickness
        self.RefractiveIndexDictionary = 0 if _refractiveindex is None else _refractiveindex
        return

    def __str__(self):
        return "The Window values are: WindowName - %s Thickness - %s  RefractiveIndex - %s" \
               % (Surface.SurfaceName, self.Thickness, self.RefractiveIndexDictionary)

    # todo def create_refractive_index_dictionary(self):
    #     return

    def calculate_mu(self, raymu):
        self.MuIn = 1/raymu
        self.MuOut = raymu/1
        return

    def get_mu_in(self):
        return self.MuIn

    def get_mu_out(self):
        return self.MuOut

    def refract_ray_at_window_surface(self, _incidentray):

        raymuu = self.RefractiveIndexDictionary.get(str(_incidentray.get_ray_wavelength()))
        self.calculate_mu(raymuu)
        if not (self.IsRayInWindow):
            _incidentray.snell_law_v2(self.get_surface_normal(), self.get_mu_in())
        else:
            _incidentray.snell_law_v2(self.get_surface_normal(), self.get_mu_out())
        self.IsRayInWindow = not self.IsRayInWindow


    def propogate_ray_to_endof_window(self, _incidentray):
        windowS2Point = self.CenterPoint + self.Normal * self.Thickness
        surface = Surface("s2", windowS2Point, self.Normal)
        print(_incidentray)
        print(surface)
        _incidentray.ray_surface_intersection(surface)

    def transmit_ray_through_window(self, _incidentray):
        self.refract_ray_at_window_surface(_incidentray)
        self.propogate_ray_to_endof_window(_incidentray)
        self.refract_ray_at_window_surface(_incidentray)
        return _incidentray

