import open3d as o3d
import numpy as np
import copy
import matplotlib.pyplot as plt


class STL():
    Filename = "Teeth"
    Path = "../src/System_Parameters/lower_jaw_tooth.stl"
    mesh = None

    def __init__(self):
        self.ObjectName = "STLObject"
        self.mesh = self.load_profile_file()

        return

    def __str__(self):
        return "Camera Name: %s "\
               % (self.ObjectName)

    def load_profile_file(self):
        file = "../src/System_Parameters/lower_jaw_tooth.stl"
        print("Testing IO for meshes ...")
        mesh = o3d.io.read_triangle_mesh(file)
        print(mesh)
        return mesh




        # %%

    def translate_STL(self, TxTyTz):
        #mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
        #mesh_tx = copy.deepcopy(mesh).translate((1.3, 0, 0))
        #mesh = self.mesh
        self.mesh = copy.deepcopy(self.mesh).translate(TxTyTz)
        print(f'Center of mesh: {self.mesh.get_center()}')
        # print(f'Center of mesh tx: {mesh_tx.get_center()}')
        # print(f'Center of mesh ty: {mesh_ty.get_center()}')
        #o3d.visualization.draw_geometries([Mesh])
        return self.mesh





    def point_cloud_plot(self, points):

        self.mesh.compute_vertex_normals()

        #hit = ans['t_hit'].isfinite()
        #points = rays[hit][:, :3] + rays[hit][:, 3:] * ans['t_hit'][hit].reshape((-1, 1))
        pcd = o3d.t.geometry.PointCloud(points)
        # Press Ctrl/Cmd-C in the visualization window to copy the current viewpoint
        o3d.visualization.draw_geometries([pcd.to_legacy()],
                                          front=[0.5, 0.86, 0.125],
                                          lookat=[0.23, 0.5, 2],
                                          up=[-0.63, 0.45, -0.63],
                                          zoom=0.7)
        return



    def rendering_3D_model(self):
        print("Computing normal and rendering it.")
        self.mesh.compute_vertex_normals()
        print(np.asarray(self.mesh.triangle_normals))
        # mesh = self.translate_STL(mesh, (18, 31, -15))
        o3d.visualization.draw_geometries([self.mesh])
        return

    def cast_rays_on_the_3D_mesh(self, raysList):

        cube = o3d.t.geometry.TriangleMesh.from_legacy(self.mesh)
        scene = o3d.t.geometry.RaycastingScene()
        vert = np.asarray(self.mesh.vertices)
        print("our vertices are: ", vert)
        cube_id = scene.add_triangles(cube)
        Rays = []
        for ray in raysList:
            holder = []
            holder.extend(ray.Origin.tolist())
            holder.extend(ray.Direction.tolist())
            #print("holder", holder)
            Rays.append(holder)
            #print("RaysList ", Rays)

        # Ray1 = [-15, -30, 0, 0, 0, -1]
        # Ray2 = [-15, 0, -5, 0, -1, 0]
        # Rays = [Ray1, Ray2]

        rays = o3d.core.Tensor(Rays, dtype=o3d.core.Dtype.Float32)
        print("our rays list", rays)
        ans = scene.cast_rays(rays)
        print("our answer is: ", ans.keys())
        print(ans['t_hit'].numpy(), ans['geometry_ids'].numpy())
        print(ans['primitive_ids'].numpy(), ans['primitive_normals'].numpy(), ans['primitive_uvs'].numpy())
        #plt.imshow(ans['t_hit'].numpy())

        updatedrayList = []
        points = []
        for index, ray in enumerate(raysList):
            print("our ray direction is:", ray.Direction, "multiplied by hit distance:", ans['t_hit'][index].numpy(), "==== ", np.dot(ray.Direction, ans['t_hit'][index].numpy()))
            print(ans['t_hit'][index].numpy())
            if ans['t_hit'][index].isfinite().numpy():
                print("we are in")
                ray.Origin = ray.Origin + np.dot(ray.Direction, ans['t_hit'][index].numpy())
                ray.write_the_story(self.ObjectName, ray.Origin, 1)
                print(ray.Origin)
                updatedrayList.append(ray)
                points.append(ray.Origin)

        #self.point_cloud_plot(points)

        return updatedrayList
    # primitives uvs = the intersection coordinates of the the ray with the mesh


    def test_rays_for_blockage(self, cameraslist):
        for camera in cameraslist:
            raysList = camera.cameraRayList

            print("We are testing blocked rays!!!")

            cube = o3d.t.geometry.TriangleMesh.from_legacy(self.mesh)
            scene = o3d.t.geometry.RaycastingScene()
            vert = np.asarray(self.mesh.vertices)
            print("our vertices are: ", vert)
            cube_id = scene.add_triangles(cube)

            Rays = []
            for ray in raysList:
                holder = []
                print("ray story coordinates", ray.RayStoryCoordinates)
                print("ray spot to ...", ray.SpottoCameraRayList)
                OriginHolder = ray.SpottoCameraRayList[1]
                DirectionHolder = (ray.SpottoCameraRayList[0]-ray.SpottoCameraRayList[1])/np.linalg.norm(ray.SpottoCameraRayList[0]-ray.SpottoCameraRayList[1])

                print(OriginHolder, DirectionHolder)
                raysegment = ray.RayStoryCoordinates[-len(ray.SpottoCameraRayList):-len(ray.SpottoCameraRayList)+2]
                Direction = raysegment[1]-raysegment[0]
                print("raysegment is: ", raysegment, "rayDirection", Direction)
                holder.extend(OriginHolder.tolist())
                holder.extend(DirectionHolder.tolist())
                # print("holder", holder)
                Rays.append(holder)

            rays = o3d.core.Tensor(Rays, dtype=o3d.core.Dtype.Float32)
            print("our rays list", rays)
            ans = scene.cast_rays(rays)
            print("our answer is: ", ans.keys())
            print(ans['t_hit'].numpy(), ans['geometry_ids'].numpy())
            print(ans['primitive_ids'].numpy(), ans['primitive_normals'].numpy(), ans['primitive_uvs'].numpy())

            updatedrayList = []
            blockedRays = []
            print("length of raylist", len(raysList))

            for index, ray in enumerate(raysList):
                # print("our ray direction is:", ray.Direction, "multiplied by hit distance:",
                #       ans['t_hit'][index].numpy(), "==== ", np.dot(ray.Direction, ans['t_hit'][index].numpy()))
                # print(ans['t_hit'][index].numpy())

                OriginP = ray.SpottoCameraRayList[0]
                OriginC = ray.SpottoCameraRayList[1] + ans['t_hit'][index].numpy()*(ray.SpottoCameraRayList[0]-ray.SpottoCameraRayList[1])/np.linalg.norm(ray.SpottoCameraRayList[0]-ray.SpottoCameraRayList[1])

                comparison = OriginP == OriginC
                print(OriginC, OriginP)
                equal_arrays = np.allclose(OriginC, OriginP, 1.e-5, 1.e-8)
                if equal_arrays:
                    print("the same location")
                else:
                    print("different location - must be a blockage")
                    raysList.remove(ray)

            print("length of raylist after", len(raysList))
            camera.cameraRayList = raysList


        return





