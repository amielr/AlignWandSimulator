from src.WandSim.Vector import Vector
from src.WandSim.Ray import Ray


class Surface:
    CenterPoint = Vector(0, 0, 0)
    Normal = Vector(0, 0, 0)
    SurfaceName = 'string'

    def __init__(self, _surfacename=None, _centralpoint=None, _normal=None):

        self.SurfaceName = "noNameWindow" if _surfacename is None else _surfacename
        self.CenterPoint = Vector(0, 0, 0) if _centralpoint is None else _centralpoint
        self.Normal = Vector(0, 0, 1) if _normal is None else _normal
        return

    def __str__(self):
        return "The object values are: SurfaceName - %s CenterPoint - %s Normal - %s" \
               % (self.SurfaceName, self.CenterPoint, self.Normal)

    def get_surface_normal(self):
        return self.Normal
