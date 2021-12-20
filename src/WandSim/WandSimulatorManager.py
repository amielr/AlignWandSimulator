from src.WandSim.SystemSetup import *
import json


with open('../src/config.json') as config_file:
    config = json.load(config_file)


def startSimulator():

    windowsList, projectorsList, reflectivesurface = create_object_lists()

    run_projectors(projectorsList)

    print("Number of projector rays is:")
    print(Projector.NoOfProjectorRays)


    propagate_rays_through_system(Projector.ProjectorRayList, windowsList, reflectivesurface)



    #rayA = Ray((0, 0, 2), (0, 0, -1), 8, 'proj1')
    rayA = Ray((-1, -2, 2), (0.3, 0, -1), 1, "proj2")

    # print("before")
    # print(rayA)
    rayA.ray_surface_intersection(windowsList[0])
    windowsList[0].transmit_ray_through_window(rayA)
    # print("after refraction at window surface", rayA)
    rayA.ray_surface_intersection(reflectivesurface[0])
    rayA.get_reflection_from_surface(reflectivesurface[0])
    print("after reflection at surface", rayA)
    return


def propagate_rays_through_system(rayList, windowsList, reflectiveSurface):
    for ray in rayList:
        ray.ray_surface_intersection(windowsList[0])
    plot_quiver(rayList)
    for ray in rayList:
        windowsList[0].transmit_ray_through_window(ray)
        # print("after refraction at window surface", rayA)
    plot_quiver(rayList)

    for ray in rayList:
        ray.ray_surface_intersection(reflectiveSurface[0])
    plot_quiver(rayList)

    for ray in rayList:
        ray.get_reflection_from_surface(reflectiveSurface[0])
    plot_quiver(rayList)

    return


