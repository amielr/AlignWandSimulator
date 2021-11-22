from src.WandSim.Ray import *
from src.WandSim.WindowLens import *


with open('../src/config.json') as config_file:
    config = json.load(config_file)

    # print(config)
    # print(json.dumps(config, indent=2))
    # print(type(config['windows']))



def startSimulator():

    WindowList = createWindows()

    print(WindowList[0])
    print(WindowList[1])

    rayA = Ray((2, 2, 2), (1, 0, 0), 8, 'proj1')
    rayB = Ray((-1, -2, -1), (0, 0, 1), 1, "proj2")


    print(rayA)
    print(rayB)

    #rayA((2,2,2),(1,0,0),8,'proj1')

    return

def createWindows():
    windowlist = []
    for window in config["windows"]:
        name, normal, center, thickness, refractiveindex = getWindowParametersFromJson(window)
        windowobject = WindowLens(name, thickness, Vector(center[0], center[1], center[2]),
                                  Vector(normal[0], normal[1], normal[2]), refractiveindex)
        windowlist.append(windowobject)
    return windowlist

def getWindowParametersFromJson(window):

        name = window["name"]
        normal = window["normal"]
        center = window["center"]
        thickness = window["thickness"]
        refractiveindex = window["refractiveindex"]
        return name, normal, center, thickness, refractiveindex


