from src.WandSim.SystemSetup import *
from src.visuliazation.PlotFunctions import plot_ray_path_line, plot_ray_locations,plot_projector_ray_locations_scatter, plot_xy_directionUnit_Projector_simulation_validation,plot_xy_Origin_Projector_simulation_validation
from copy import deepcopy
import time


def startSimulator():
    print("start of round")
    windowsList, projectorsList, reflectivesurface, STLSurface, cameraList = create_object_lists()

    run_projectors(projectorsList)

    begin = time.time()

    propagate_rays_through_system(windowsList, reflectivesurface, projectorsList, cameraList)
    end = time.time()
    total_no_windows_time = end - begin
    print("Total time for regular run", total_no_windows_time)

    begin = time.time()
    propagate_rays_through_system_no_windows(reflectivesurface, projectorsList, cameraList)
    end = time.time()

    total_no_windows_time = end - begin

    print("Total time for no windows", total_no_windows_time)
    #propagate_rays_through_system_STL(Projector, windowsList, STLSurface, projectorsList, cameraList)

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


def propagate_rays_to_reflective_surface_no_windows(reflectiveSurface, projectorList):
    Projector.AllProjectorRaysList.clear()
    for projector in projectorList:
        for ray in projector.ProjectorRayList:

            ray.ray_surface_intersection(reflectiveSurface[0])
            # print("our object type is: ", type(reflectiveSurface[0]))
            # print(isinstance(reflectiveSurface[0], WindowLens))
            Projector.AllProjectorRaysList.append(ray)

    #plot_ray_locations(Projector.AllProjectorRaysList)
    #plot_ray_path_line(Projector.AllProjectorRaysList)
    # plot_projector_ray_locations_scatter(projector)
    # plot_quiver(projector.ProjectorRayList, windowsList[0].SurfaceName + " before")
    # plot_quiver(Projector.AllProjectorRaysList, windowsList[0].Name + "full raylist")



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
    for surface in surfaceList:
        distance = np.linalg.norm(ray.Origin-surface.CenterPoint)
        distanceList.append(distance)
        # print(str(surface.Name) + " distance from ray origin to surface: " + str(distance))

    sortedSurfacesList = [x for _, x in sorted(zip(distanceList, surfaceList))]
    # [print(surfaceholder.CenterPoint) for surfaceholder in sortedSurfacesList]
    return sortedSurfacesList



def propagate_rays_back_to_cameras(cameraList, windowsList):
    for camera in cameraList:
        windowsList.append(camera.window)
        print("camera window parameters", camera.window)
        print("camera direction: ", camera.center, camera.direction)
        camera.cameraRayList = []
        projectorRaylistscopy = deepcopy(Projector.AllProjectorRaysList)
        for ray in projectorRaylistscopy:
            camera.cameraRayList.append(camera.get_initial_intersection_points_from_surface_to_camera_v2(ray, windowsList))

        #print("Ray Initial conditions:  tell the story...", ray.tell_the_story())
        #plot_ray_path_line(camera.cameraRayList)
        camera.optimize_Camera_rays()

        #plot_ray_path_line(camera.cameraRayList)
        windowsList.remove(camera.window)
        camera.determine_pixel_locations()



def propagate_rays_back_to_cameras_no_windows(cameraList):
    for camera in cameraList:
        print("camera window parameters", camera.window)
        print("camera center and direction: ", camera.center, camera.direction)
        camera.cameraRayList = []

        projectorRaylists = deepcopy(Projector.AllProjectorRaysList)

        for ray in projectorRaylists:
            #raycopy = deepcopy(ray)
            camera.cameraRayList.append(camera.get_intersection_with_camera_no_windows(ray))

        #print("Ray Initial conditions:  tell the story...", ray.tell_the_story())
        #plot_ray_path_line(camera.cameraRayList)
        #camera.optimize_Camera_rays()

        #plot_ray_path_line(camera.cameraRayList)
        #camera.determine_pixel_locations()



def propagate_rays_through_system_no_windows(reflectiveSurface, projectorList, cameraList):
    propagate_rays_to_reflective_surface_no_windows(reflectiveSurface, projectorList)
    propagate_rays_back_to_cameras_no_windows(cameraList)


def propagate_rays_through_system(windowsList, reflectiveSurface, projectorList, cameraList):

    propagate_rays_to_reflective_surface(windowsList, reflectiveSurface, projectorList)

    #plot_projector_ray_locations_scatter(projectorList[0])
    # my_data = genfromtxt('../src/Validation/B2-ITO-Directions.csv', delimiter=',', skip_header=1)
    # Xvalidation = my_data[:, 0]-0.01
    # Yvalidation = my_data[:, 1]-0.017
    #
    my_data = genfromtxt('../src/Validation/B2-132mm.csv', delimiter=',', skip_header=1)
    Xvalidation = my_data[:, 0]
    Yvalidation = my_data[:, 1]
    #plot_xy_directionUnit_Projector_simulation_validation(projectorList[0], Xvalidation, Yvalidation)

    #plot_xy_Origin_Projector_simulation_validation(projectorList[0], Xvalidation, Yvalidation)



    propagate_rays_back_to_cameras(cameraList, windowsList)
    return


def propagate_rays_to_reflective_surface_STL(windowsList, reflectiveSurface, projectorList):
    Projector.AllProjectorRaysList.clear()
    for projector in projectorList:
        for ray in projector.ProjectorRayList:
            sortedwindowsList = reorder_list_from_closest_to_furthest(ray, windowsList)

            for window in sortedwindowsList:
                sortedSurfaceList = reorder_list_from_closest_to_furthest(ray, window.surfaceList)
                window.surfaceList = sortedSurfaceList

                ray_window_manager(ray, window)

            Projector.AllProjectorRaysList.append(ray)
    mesh = reflectiveSurface.load_profile_file()
    print("our mesh is", mesh)
    Projector.AllProjectorRaysList = reflectiveSurface.cast_rays_on_the_3D_mesh(Projector.AllProjectorRaysList)
    print("projector rays list: ", Projector.AllProjectorRaysList)
    print("projector ray origin: ", Projector.AllProjectorRaysList[0].Origin)
    #reflectiveSurface.rendering_3D_model()
    #plot_ray_locations(Projector.AllProjectorRaysList)
    #plot_projector_ray_locations_scatter(Projector)
    #plot_quiver(projector.ProjectorRayList, windowsList[0].SurfaceName + " before")
    #plot_quiver(Projector.AllProjectorRaysList, windowsList[0].Name + "full raylist")


def propagate_rays_through_system_STL(Projector, windowsList, reflectiveSurface, projectorList, cameraList):

    propagate_rays_to_reflective_surface_STL(windowsList, reflectiveSurface, projectorList)
    propagate_rays_back_to_cameras(cameraList, windowsList)
    reflectiveSurface.test_rays_for_blockage(cameraList)
    #plot_ray_path_line(cameraList[0].cameraRayList)
    return


