import numpy as np



class Surface:
    CenterPoint = np.array([0, 0, 0])
    Normal = np.array([0, 0, 0])
    Name = 'string'

    def __init__(self, _surfacename=None, _centralpoint=None, _normal=None):

        self.Name = "noName" if _surfacename is None else _surfacename
        self.CenterPoint = np.array([0, 0, 0]) if _centralpoint is None else _centralpoint
        self.Normal = np.array([0, 0, 1]) if _normal is None else _normal
        return

    def __str__(self):
        return "The object values are: SurfaceName - %s CenterPoint - %s Normal - %s" \
               % (self.Name, self.CenterPoint, self.Normal)

    def get_surface_normal(self):
        return self.Normal

    def determine_surface_z_given_xy(self, XY):
        x = XY[0]
        y = XY[1]
        surfacXYZ = self.Normal
        Dfactor = np.dot(self.Normal, self.CenterPoint)
        z = (-surfacXYZ[0]*x -surfacXYZ[1]*y + Dfactor)/surfacXYZ[2]
        return z



