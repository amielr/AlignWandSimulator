from src.WandSim.Ray import *
from src.WandSim.WindowLens import *
import json


with open('../src/config.json') as config_file:
    config = json.load(config_file)

    # print(config)
    # print(json.dumps(config, indent=2))
    # print(type(config['windows']))



def startSimulator():

    windowList = create_windows()

    rayA = Ray((2, 2, 2), (0, 0, -1), 8, 'proj1')
    rayB = Ray((-1, -2, 2), (0.3, 0, -1), 1, "proj2")

    # todo rayList = create_rays()
    print("before")
    print(rayA)
    print(rayB)
    rayA = windowList[0].transmit_ray_through_window(rayA)
    rayB = windowList[0].transmit_ray_through_window(rayB)
    print("after")
    print(rayA)
    print(rayB)


    #rayA((2,2,2),(1,0,0),8,'proj1')

    return

def create_windows():
    windowlist = []
    for window in config["windows"]:
        name, normal, center, thickness, refractiveindex = get_window_parameters_from_json(window)
        windowobject = WindowLens(name, thickness, Vector(center[0], center[1], center[2]),
                                  Vector(normal[0], normal[1], normal[2]), refractiveindex)
        windowlist.append(windowobject)
    return windowlist

def get_window_parameters_from_json(window):

        name = window["name"]
        normal = window["normal"]
        center = window["center"]
        thickness = window["thickness"]
        refractiveindex = window["refractiveindex"]
        return name, normal, center, thickness, refractiveindex


