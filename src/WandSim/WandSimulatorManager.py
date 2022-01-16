from src.WandSim.SystemSetup import *


def startSimulator():

    windowsList, projectorsList, reflectivesurface, cameraList = create_object_lists()

    run_projectors(projectorsList)

    propagate_rays_through_system(Projector, windowsList, reflectivesurface, projectorsList)


    print("Number of projector rays is:")
    print(Projector.NoOfProjectorRays)

    print(cameraList[0].fermatManager(Projector.AllProjectorRaysList[1], windowsList[0]))

    # print(cameraList[0])
    #
    # print(cameraList[0].worldToCamera)
    #
    # print(np.matmul(cameraList[0].cameraLocalToWorld, cameraList[0].worldToCamera))




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


def propagate_rays_through_system(Projector, windowsList, reflectiveSurface, projectorList):

    #rayList = Projector.AllProjectorRaysList
    Projector.AllProjectorRaysList.clear()
    for projector in projectorList:
        for ray in projector.ProjectorRayList:
            ray.ray_surface_intersection(windowsList[0])
            windowsList[0].transmit_ray_through_window(ray)
            ray.ray_surface_intersection(reflectiveSurface[0])


            Projector.AllProjectorRaysList.append(ray)
    plot_projector_ray_locations_scatter(projector)
    #plot_quiver(projector.ProjectorRayList, windowsList[0].SurfaceName + " before")
    plot_quiver(Projector.AllProjectorRaysList, windowsList[0].SurfaceName+"full raylist")


    # for ray in rayList:
    #     ray.get_reflection_from_surface(reflectiveSurface[0])
    # plot_quiver(rayList, reflectiveSurface[0].SurfaceName)

    for ray in Projector.AllProjectorRaysList:
        ray.tell_the_story()
        ray.print_the_story()

    return


