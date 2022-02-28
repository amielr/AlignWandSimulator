from src.WandSim.SystemSetup import *



def startSimulator():
    print("start of round")
    windowsList, projectorsList, reflectivesurface, cameraList = create_object_lists()

    run_projectors(projectorsList)

    propagate_rays_through_system(Projector, windowsList, reflectivesurface, projectorsList, cameraList)

    #reflectivesurface[0].load_profile_file()

    #plot_ray_path_line(Projector.AllProjectorRaysList)
    #print("Number of projector rays is:")
    #print(Projector.NoOfProjectorRays)
    return


def ray_window_manager(ray, window):
    ray.IsRayInWindow = not ray.IsRayInWindow
    window.ray_window_refractive_registration(ray)
    ray.ray_surface_intersection(window.surfaceList[0])
    # print("our object type is: ", type(window))
    # print(isinstance(window, WindowLens))
    window.transmit_ray_through_window(ray)
    # ray.IsRayInWindow = not ray.IsRayInWindow
    # window.ray_window_refractive_registration(ray)
    return


def propagate_rays_to_reflective_surface(windowsList, reflectiveSurface, projectorList):
    # rayList = Projector.AllProjectorRaysList
    Projector.AllProjectorRaysList.clear()
    for projector in projectorList:
        for ray in projector.ProjectorRayList:
            sortedwindowsList = reorder_list_from_closest_to_furthest(ray, windowsList)

            for window in sortedwindowsList:
                sortedSurfaceList = reorder_list_from_closest_to_furthest(ray, window.surfaceList)
                window.surfaceList = sortedSurfaceList

                ray_window_manager(ray, window)


            ray.ray_surface_intersection(reflectiveSurface[0])
            ray.get_reflection_from_surface(reflectiveSurface[0])
            #print("our object type is: ", type(reflectiveSurface[0]))
            #print(isinstance(reflectiveSurface[0], WindowLens))
            Projector.AllProjectorRaysList.append(ray)

    #plot_ray_locations(Projector.AllProjectorRaysList)
    # plot_projector_ray_locations_scatter(projector)
    # plot_quiver(projector.ProjectorRayList, windowsList[0].SurfaceName + " before")
    #plot_quiver(Projector.AllProjectorRaysList, windowsList[0].Name + "full raylist")


def reorder_list_from_closest_to_furthest(ray, surfaceList):
    distanceList = []
    flag = False
    for surface in surfaceList:
        distance = np.linalg.norm(ray.Origin-surface.CenterPoint)
        distanceList.append(distance)
        print(str(surface.Name) + " distance from ray origin to surface: " + str(distance))

    sortedSurfacesList = [x for _, x in sorted(zip(distanceList, surfaceList))]
    [print(surfaceholder.CenterPoint) for surfaceholder in sortedSurfacesList]
    return sortedSurfacesList

def propagate_rays_back_to_cameras(cameraList, windowsList):
    for camera in cameraList:
        windowsList.append(camera.window)
        camera.cameraRayList = camera.get_initial_intersection_points_from_surface_to_camera(Projector.AllProjectorRaysList, windowsList)
        windowsList.remove(camera.window)
        camera.optimize_Camera_rays()
        camera.determine_pixel_locations()

    # for camera in cameraList:
    #     plot_ray_path_line(camera.cameraRayList)


def propagate_rays_through_system(Projector, windowsList, reflectiveSurface, projectorList, cameraList):

    propagate_rays_to_reflective_surface(windowsList, reflectiveSurface, projectorList)
    propagate_rays_back_to_cameras(cameraList, windowsList)
    # for ray in rayList:
    #     ray.get_reflection_from_surface(reflectiveSurface[0])
    # plot_quiver(rayList, reflectiveSurface[0].SurfaceName)
    # for camera in cameraList:
    #     for ray in camera.cameraRayList:
    # #for ray in Projector.AllProjectorRaysList:
    #         ray.tell_the_story()
    #         ray.print_the_story()
    return




