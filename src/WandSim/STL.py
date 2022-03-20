import open3d as o3d
import numpy as np
import copy
import matplotlib.pyplot as plt


class STL():
    Filename = "Teeth"
    Path = "../src/System_Parameters/lower_jaw_tooth.stl"
    mesh = None

    def __init__(self):
        self.cameraName = "noName"
        self.mesh = self.load_profile_file()

        return

    def __str__(self):
        return "Camera Name: %s "\
               % (self.cameraName)

    def load_profile_file(self):
        file = "../src/System_Parameters/lower_jaw_tooth.stl"
        print("Testing IO for meshes ...")
        mesh = o3d.io.read_triangle_mesh(file)
        print(mesh)
        return mesh


    def rendering_3D_model(self, mesh):
        print("Computing normal and rendering it.")
        mesh.compute_vertex_normals()
        print(np.asarray(mesh.triangle_normals))
        #mesh = self.translate_STL(mesh, (18, 31, -15))
        o3d.visualization.draw_geometries([mesh])
        return

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
        #
        # Rays = [Ray1, Ray2]

        rays = o3d.core.Tensor(Rays, dtype=o3d.core.Dtype.Float32)
        print("our rays list", rays)
        ans = scene.cast_rays(rays)
        print("our answer is: ", ans.keys())
        print(ans['t_hit'].numpy(), ans['geometry_ids'].numpy())
        print(ans['primitive_ids'].numpy(), ans['primitive_normals'].numpy(), ans['primitive_uvs'].numpy())

        updatedrayList = []
        for index, ray in enumerate(raysList):
            print("our ray direction is:", ray.Direction, "multiplied by hit distance:",ans['t_hit'][index].numpy(), "==== ", np.dot(ray.Direction, ans['t_hit'][index].numpy()))
            print(ans['t_hit'][index])
            ray.Origin = ray.Origin + np.dot(ray.Direction, ans['t_hit'][index].numpy())
            updatedrayList.append(ray)

        return updatedrayList
    # primitives uvs = the intersection coordinates of the the ray with the mesh

    # %%




