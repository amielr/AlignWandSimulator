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

    #rayA = Ray((0, 0, 2), (0, 0, -1), 8, 'proj1')
    rayA = Ray((-1, -2, 2), (0.3, 0, -1), 1, "proj2")

    reflectivesurface = create_surfaces()

    # todo rayList = create_rays()
    print("before")
    print(rayA)
    rayA.ray_surface_intersection(windowList[0])
    windowList[0].transmit_ray_through_window(rayA)
    print("after refraction at window surface", rayA)
    rayA.ray_surface_intersection(reflectivesurface[0])
    rayA.get_reflection_from_surface(reflectivesurface[0])
    print("after reflection at surface", rayA)



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


def create_surfaces():
    surfaceList = []
    for surface in config["surfaces"]:
        name, normal, center = get_surface_parameters_from_json(surface)
        surfaceobject = Surface(name, Vector(center[0], center[1], center[2]),
                                  Vector(normal[0], normal[1], normal[2]))
        surfaceList.append(surfaceobject)
    return surfaceList


def get_surface_parameters_from_json(surface):
        name = surface["name"]
        normal = surface["normal"]
        center = surface["center"]
        return name, normal, center
