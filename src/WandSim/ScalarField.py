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


#       gaussX = np.exp(-(Xrange ** 2 / (2.0 * Sigma ** 2)))
#       gaussY = np.exp(-(Yrange ** 2 / (2.0 * Sigma ** 2)))
#       gauss = gaussX*gaussY
