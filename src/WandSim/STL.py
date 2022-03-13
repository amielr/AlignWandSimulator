import open3d as o3d
import numpy as np



def load_profile_file():
    file = "../src/System_Parameters/lower_jaw_tooth.stl"
    print("Testing IO for meshes ...")
    mesh = o3d.io.read_triangle_mesh(file)
    print(mesh)
    return mesh


def rendering_3D_model(mesh):
    print("Computing normal and rendering it.")
    mesh.compute_vertex_normals()
    print(np.asarray(mesh.triangle_normals))
    o3d.visualization.draw_geometries([mesh])

    # %%

def cast_rays_on_the_3D_mesh(mesh, raysList):

    cube = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
    scene = o3d.t.geometry.RaycastingScene()
    cube_id = scene.add_triangles(cube)
    Rays = []
    for ray in raysList:
        holder = [ray.Origin, ray.Direction]
        Rays.append(holder)

    # Ray1 = [-15, -30, 0, 0, 0, -1]
    # Ray2 = [-15, 0, -5, 0, -1, 0]
    #
    # Rays = [Ray1, Ray2]

    rays = o3d.core.Tensor(Rays, dtype=o3d.core.Dtype.Float32)
    print(rays)
    ans = scene.cast_rays(rays)
    print("our answer is: ", ans.keys())
    print(ans['t_hit'].numpy(), ans['geometry_ids'].numpy())
    print(ans['primitive_ids'].numpy(), ans['primitive_normals'].numpy(), ans['primitive_uvs'].numpy())

    raysList = [ray.Origin + ray.Direction*distance for distance, ray in zip(ans['t_hit'] ,raysList)]

    for index, ray in enumerate(raysList):
        ray.Origin = ray.Origin + ray.Direction * ans['t_hit'][index]

    return raysList
    # primitives uvs = the intersection coordinates of the the ray with the mesh

    # %%



    import matplotlib.pyplot as plt

    # %%
    # getting vertices and triangles
    vert = np.asarray(mesh.vertices)
    tri = np.asarray(mesh.triangles)

    print("triangle data")
    print(mesh.triangles)
    print(tri)
    ax = plt.axes(projection='3d')
    x, y, z = vert[::100, 0], vert[::100, 1], vert[::100, 2]
    ax.plot_trisurf(x, y, z,
                    cmap='viridis', edgecolor='none');
    return
