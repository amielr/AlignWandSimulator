import numpy as np
import json
import math


with open('../src/config.json') as config_file:
    config = json.load(config_file)


def get_lattice_const():
    return config["LatticeConst"]



class ScalarField:

    def __init__(self):
        self._xGrid = []
        self._yGrid = []
        self._zScalarField = []

    def grating_kernel(self):
        return


    def grating_grid(self):
        coordinateConstant = get_lattice_const()
        density = coordinateConstant

        Xgrid = np.arange(-2*coordinateConstant, 2*coordinateConstant+density, density/8)
        self._xGrid, self._yGrid = np.meshgrid(Xgrid, Xgrid)
        self._zScalarField = np.zeros(self._xGrid.shape)
        return self._xGrid, self._yGrid, self._zScalarField


    def grating_degree(self, n, m, gratingdistance):
        isFlagOdd = False
        for y in range(m):
            ycoordinate = y * gratingdistance
            isFlagOdd = not isFlagOdd
            for x in range(n):
                if isFlagOdd:
                    xcoordinate = x*gratingdistance + gratingdistance/2
                else:
                    xcoordinate = x * gratingdistance
                self._zScalarField = np.add(self._zScalarField,
                                            (np.where(self._xGrid == xcoordinate, 1, 0) & np.where(self._yGrid == ycoordinate, 1, 0)))

        return self._xGrid, self._yGrid, self._zScalarField

#       gaussX = np.exp(-(Xrange ** 2 / (2.0 * Sigma ** 2)))
#       gaussY = np.exp(-(Yrange ** 2 / (2.0 * Sigma ** 2)))
#       gauss = gaussX*gaussY
