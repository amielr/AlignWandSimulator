from src.WandSim.Vector import Vector
import json


class WindowLens:

    #Width, Length = 0, 0
    RefractiveIndexDictionary = {''}
    Thickness = 0
    #Point1, Point2, Point3 = Vector(0, 0, 0), Vector(0, 0, 0), Vector(0, 0, 0)
    CenterPoint = Vector(0, 0, 0)
    Normal = Vector(0, 0, 0)
    WindowName = 'string'

    def __init__(self, _windowname=None, _thickness=None, _centralpoint=None, _normal=None, _refractiveindex=None):

        self.WindowName = "noNameWindow" if _windowname is None else _windowname
        self.Thickness = 0 if _thickness is None else _thickness
        self.CenterPoint = (0, 0, 0) if _centralpoint is None else _centralpoint
        self.Normal = (0, 0, 1) if _normal is None else _normal
        self.RefractiveIndexDictionary = 0 if _refractiveindex is None else _refractiveindex

        return

    def __str__(self):
        return "The object values are: WindowName - %s Thickness - %s CenterPoint - %s Normal - %s RefractiveIndex - %s" \
               % (self.WindowName, self.Thickness, self.CenterPoint, self.Normal, self.RefractiveIndexDictionary)



    def create_refractive_index_dictionary(self):
        return

    def set_window_parameters(self, _width, _length, _thickness):
        self.Width = _width
        self.Length = _length
        self.Thickness = _thickness
        return

    def set_window_location(self):
        self.Point1 = Vector()
        return

    def set_refractive_index(self):

        return

    def calculate_mu(self):
        return

    def calculate_window_normal(self):
        return

    def transfer_ray(self, _incidentray):

        return


