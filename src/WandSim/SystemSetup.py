from src.WandSim.Projector import *
from src.WandSim.Camera import *



def run_projectors(projectorsList):
    for projector in projectorsList:
        projector.generate_projector_rays()
    #    plot_quiver(projector.ProjectorRayList, str(projector.projectorName))
    #plot_quiver(Projector.AllProjectorRaysList, str(Projector.projectorName))


def create_object_lists():
    windowList = create_windows()
    reflectivesurface = create_surfaces()
    projectors = create_projectors()
    camerasList = create_cameras()

    return windowList, projectors, reflectivesurface, camerasList


def create_windows():
    windowlist = []
    for window in config["windows"]:
        name, normal, center, thickness, refractiveindex = get_window_parameters_from_json(window)
        windowobject = WindowLens(name, thickness, np.array([center[0], center[1], center[2]]),
                                  np.array([normal[0], normal[1], normal[2]]), refractiveindex)
        windowlist.append(windowobject)

    return windowlist


def get_window_parameters_from_json(window):

    name = window["name"]
    normal = window["normal"]
    center = window["center"]
    thickness = window["thickness"]
    refractiveindex = window["refractiveindex"]
    #print("refractive index is: ", refractiveindex)

    return name, normal, center, thickness, refractiveindex


def create_surfaces():
    surfaceList = []
    for surface in config["surfaces"]:
        name, normal, center = get_surface_parameters_from_json(surface)
        surfaceobject = Surface(name, np.array([center[0], center[1], center[2]]),
                                  np.array([normal[0], normal[1], normal[2]]))
        surfaceList.append(surfaceobject)
    return surfaceList


def get_surface_parameters_from_json(surface):
        name = surface["name"]
        normal = surface["normal"]
        center = surface["center"]
        return name, normal, center


def create_projectors():
    projectorList = []
    for projector in config["lights"]:
        name, center, direction, rotation, wavelength, projtype, gratingorder, latticeconstant, OnOff = get_projector_parameters_from_json(projector)

        if OnOff=="On":
            projectorobject = Projector(name, center, direction, rotation, wavelength, projtype, gratingorder, latticeconstant)
            projectorList.append(projectorobject)

    if len(projectorList) == 0:
        print("Huston we have a problem the projector list is of len:", len(projectorList))
        exit()
    return projectorList


def get_projector_parameters_from_json(projector):
    name = projector["name"]
    rotation = projector["rotation"]
    center = projector["center"]
    direction = projector["direction"]
    wavelength = projector["wavelength"]
    projtype = projector["type"]
    gratingorder = projector["GratingOrder"]
    latticConstant = projector["LatticeConst"]
    OnOff = projector["OnOff"]
    return name, center, direction, rotation, wavelength, projtype, gratingorder, latticConstant, OnOff


def create_cameras():
    cameraList = []
    for camera in config["cameras"]:
        name, center, direction, rotation, cameratype, windowthickness, refractiveindex, OnOff  = get_camera_parameters_from_json(camera)

        if OnOff == "On":
            cameraobject = Camera(name, center, direction,
                                        rotation, cameratype, windowthickness, refractiveindex)
            #windowobject = WindowLens(name+"window", windowthickness, center+direction, direction, refractiveindex)
            cameraList.append(cameraobject)
    if len(cameraList) == 0:
        print("Huston we have a problem the Camera list is of len:", len(cameraList))
        exit()
    return cameraList


def get_camera_parameters_from_json(camera):
    name = camera["name"]
    center = camera["center"]
    direction = camera["direction"]
    rotation = camera["rotation"]
    cameratype = camera["type"]
    windowthickness = camera["thickness"]
    refractiveindex = camera["refractiveindex"]
    OnOff = camera["OnOff"]


    return name, center, direction, rotation, cameratype, windowthickness, refractiveindex, OnOff
