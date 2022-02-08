from src.WandSim.SystemSetup import *


def startSimulator():

    windowsList, projectorsList, reflectivesurface, cameraList = create_object_lists()

    run_projectors(projectorsList)

    propagate_rays_through_system(Projector, windowsList, reflectivesurface, projectorsList, cameraList)

    plot_ray_path_line(Projector.AllProjectorRaysList)


    print("Number of projector rays is:")
    print(Projector.NoOfProjectorRays)


    return



def propagate_rays_to_reflective_surface(windowsList, reflectiveSurface, projectorList):
    # rayList = Projector.AllProjectorRaysList
    Projector.AllProjectorRaysList.clear()
    for projector in projectorList:
        for ray in projector.ProjectorRayList:
            for window in windowsList:
                ray.ray_surface_intersection(window)
                window.transmit_ray_through_window(ray)
            ray.ray_surface_intersection(reflectiveSurface[0])

            Projector.AllProjectorRaysList.append(ray)

    #plot_ray_locations(Projector.AllProjectorRaysList)
    # plot_projector_ray_locations_scatter(projector)
    # plot_quiver(projector.ProjectorRayList, windowsList[0].SurfaceName + " before")
    plot_quiver(Projector.AllProjectorRaysList, windowsList[0].SurfaceName + "full raylist")

def propagate_rays_back_to_cameras(cameraList, windowsList):
    for camera in cameraList:
        camera.CameraDotRayList = camera.get_initial_intersection_points_from_surface_to_camera(Projector.AllProjectorRaysList, windowsList)


def propagate_rays_through_system(Projector, windowsList, reflectiveSurface, projectorList, cameraList):

    propagate_rays_to_reflective_surface(windowsList, reflectiveSurface, projectorList)
    propagate_rays_back_to_cameras(cameraList, windowsList)
    # for ray in rayList:
    #     ray.get_reflection_from_surface(reflectiveSurface[0])
    # plot_quiver(rayList, reflectiveSurface[0].SurfaceName)

    for ray in Projector.AllProjectorRaysList:
        ray.tell_the_story()
        ray.print_the_story()

    return


