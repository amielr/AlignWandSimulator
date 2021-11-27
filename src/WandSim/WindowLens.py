from src.WandSim.Vector import Vector
from src.WandSim.Ray import Ray


class WindowLens:

    #todo change refractive index to dictionary for different wavelengths
    RefractiveIndexDictionary = 0
    Thickness = 0
    CenterPoint = Vector(0, 0, 0)
    Normal = Vector(0, 0, 0)
    WindowName = 'string'
    MuIn = 0
    MuOut = 0

    def __init__(self, _windowname=None, _thickness=None, _centralpoint=None, _normal=None, _refractiveindex=None):

        self.WindowName = "noNameWindow" if _windowname is None else _windowname
        self.Thickness = 0 if _thickness is None else _thickness
        self.CenterPoint = Vector(0, 0, 0) if _centralpoint is None else _centralpoint
        self.Normal = Vector(0, 0, 1) if _normal is None else _normal
        self.RefractiveIndexDictionary = 0 if _refractiveindex is None else _refractiveindex
        return

    def __str__(self):
        return "The object values are: WindowName - %s Thickness - %s CenterPoint - %s Normal - %s RefractiveIndex - %s" \
               % (self.WindowName, self.Thickness, self.CenterPoint, self.Normal, self.RefractiveIndexDictionary)

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

    def get_window_normal(self):
        return self.Normal

    def transmit_ray_through_window(self, _incidentray):
        #print(_incidentray.get_ray_wavelength())
        raymuu = self.RefractiveIndexDictionary.get(str(_incidentray.get_ray_wavelength()))
        self.calculate_mu(raymuu)

        _incidentray.snell_law(self.get_window_normal(), self.get_mu_in())

        #_incidentray.snell_refraction(self.get_window_normal(), self.get_mu_in())

        return _incidentray


