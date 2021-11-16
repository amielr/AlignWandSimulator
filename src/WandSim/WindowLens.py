from src.WandSim.Vector import Vector
import json


thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}


with open('../config.json') as config_file:
    config = json.load(config_file)


class WindowLens():

    Width, Length, Thickness = 0, 0, 0
    RefractiveIndexDictionary = {}
    Point1, Point2, Point3 = Vector(0, 0, 0), Vector(0, 0, 0), Vector(0, 0, 0)
    Normal = Vector(0, 0, 0)
    WindowName = 'string'

    def __init__(self):

        return

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


