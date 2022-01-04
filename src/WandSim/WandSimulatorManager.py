from src.WandSim.SystemSetup import *


def startSimulator():

    windowsList, projectorsList, reflectivesurface, cameraList = create_object_lists()

    #run_projectors(projectorsList)

    print("Number of projector rays is:")
    print(Projector.NoOfProjectorRays)


    print(cameraList[0])

    #propagate_rays_through_system(Projector.ProjectorRayList, windowsList, reflectivesurface)



    #rayA = Ray((0, 0, 2), (0, 0, -1), 8, 'proj1')
    # rayA = Ray((-1, -2, 2), (0, 1, -1), 1, "proj2")
    #
    # print("before", rayA)
    #
    # rayA.ray_surface_intersection(windowsList[0])
    # print("ray at window s1 surface", rayA)
    # windowsList[0].transmit_ray_through_window(rayA)
    # print("after transmission at window surface", rayA)
    # rayA.ray_surface_intersection(reflectivesurface[0])
    # rayA.get_reflection_from_surface(reflectivesurface[0])
    # print("after reflection at surface", rayA)
    return


def propagate_rays_through_system(rayList, windowsList, reflectiveSurface):
    for ray in rayList:
        ray.ray_surface_intersection(windowsList[0])
    plot_quiver(rayList, windowsList[0].SurfaceName + " before")
    beforelist = rayList.copy()
    for ray in rayList:
        windowsList[0].transmit_ray_through_window(ray)
        # print("after refraction at window surface", rayA)
    plot_quiver(rayList, windowsList[0].SurfaceName + " after" )

    for ray in rayList:
        ray.ray_surface_intersection(reflectiveSurface[0])
    plot_quiver(rayList, reflectiveSurface[0].SurfaceName)

    for ray in rayList:
        ray.get_reflection_from_surface(reflectiveSurface[0])
    plot_quiver(rayList, reflectiveSurface[0].SurfaceName)

    # for ray in rayList:
    #     ray.print_story()

    return


