import numpy as np
import open3d as o3d



class Surface:
    CenterPoint = np.array([0, 0, 0])
    Normal = np.array([0, 0, 0])
    Name = 'string'

    def __init__(self, _surfacename=None, _centralpoint=None, _normal=None):

        self.Name = "noName" if _surfacename is None else _surfacename
        self.CenterPoint = np.array([0, 0, 0]) if _centralpoint is None else _centralpoint
        self.Normal = np.array([0, 0, 1]) if _normal is None else _normal
        return

    def __str__(self):
        return "The object values are: SurfaceName - %s CenterPoint - %s Normal - %s" \
               % (self.Name, self.CenterPoint, self.Normal)

    def get_surface_normal(self):
        return self.Normal

    def determine_surface_z_given_xy(self, XY):
        x = XY[0]
        y = XY[1]
        surfacXYZ = self.Normal
        Dfactor = np.dot(self.Normal, self.CenterPoint)
        z = (-surfacXYZ[0]*x -surfacXYZ[1]*y + Dfactor)/surfacXYZ[2]
        return z

    def load_profile_file(self):
        file = "../src/System_Parameters/lower_jaw_tooth.stl"
        print("Testing IO for meshes ...")
        mesh = o3d.io.read_triangle_mesh(file)
        print(mesh)

        # %%
        # getting vertices and triangles
        vert = np.asarray(mesh.vertices)
        tri = np.asarray(mesh.triangles)

        print("triangle data")
        print(mesh.triangles)
        print(tri)

        # %%

        # rendering 3D model
        print("Computing normal and rendering it.")
        mesh.compute_vertex_normals()
        print(np.asarray(mesh.triangle_normals))


        o3d.visualization.draw_geometries([mesh])

        # %%

        # casting rays on the 3D mesh

        cube = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
        scene = o3d.t.geometry.RaycastingScene()
        cube_id = scene.add_triangles(cube)
        Ray1 = [-15, -30, 0, 0, 0, -1]
        Ray2 = [-15, 0, -5, 0, -1, 0]

        Rays = [Ray1, Ray2]

        rays = o3d.core.Tensor(Rays, dtype=o3d.core.Dtype.Float32)
        ans = scene.cast_rays(rays)
        print("our answer is: ", ans.keys())
        print(ans['t_hit'].numpy(), ans['geometry_ids'].numpy())
        print(ans['primitive_ids'].numpy(), ans['primitive_normals'].numpy(), ans['primitive_uvs'].numpy())

        # primitives uvs = the intersection coordinates of the the ray with the mesh

        # %%
        import matplotlib.pyplot as plt
        ax = plt.axes(projection='3d')
        x, y, z = vert[::100, 0], vert[::100, 1], vert[::100, 2]
        ax.plot_trisurf(x, y, z,
                        cmap='viridis', edgecolor='none');
        return


