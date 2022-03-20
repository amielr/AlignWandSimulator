from src.WandSim.Projector import *
from src.WandSim.Camera import *
from src.WandSim.STL import STL



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
    STLobject = create_STL_object()



    return windowList, projectors, reflectivesurface,STLobject, camerasList

def create_STL_object():
    STLobject = STL()
    STLobject.translate_STL((18, 20, -15))
    print("have we translated", np.asarray(STLobject.mesh.vertices))
    return STLobject


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
        name, center, direction, rotation, wavelength, projtype, gratingorder, latticeconstant = get_projector_parameters_from_json(projector)

        projectorobject = Projector(name, center, direction, rotation, wavelength, projtype, gratingorder, latticeconstant)
        projectorList.append(projectorobject)
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
    return name, center, direction, rotation, wavelength, projtype, gratingorder, latticConstant


def create_cameras():
    cameraList = []
    for camera in config["cameras"]:
        name, center, direction, rotation, cameratype, windowthickness, refractiveindex  = get_camera_parameters_from_json(camera)

        cameraobject = Camera(name, center, direction,
                                    rotation, cameratype, windowthickness, refractiveindex)
        #windowobject = WindowLens(name+"window", windowthickness, center+direction, direction, refractiveindex)
        cameraList.append(cameraobject)
    return cameraList


def get_camera_parameters_from_json(camera):
    name = camera["name"]
    center = camera["center"]
    direction = camera["direction"]
    rotation = camera["rotation"]
    cameratype = camera["type"]
    windowthickness = camera["thickness"]
    refractiveindex = camera["refractiveindex"]

    return name, center, direction, rotation, cameratype, windowthickness, refractiveindex
