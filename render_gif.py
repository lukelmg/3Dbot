import sys
import trimesh
import pyrender
import numpy as np
import imageio

inp = sys.argv[1]
outp = sys.argv[2]

mesh = trimesh.load_mesh(inp)
mesh.apply_translation(-mesh.centroid)

# distance from model to camera
extent = float(np.max(mesh.extents))*1.5

material = pyrender.MetallicRoughnessMaterial(
    baseColorFactor=[0.1, 0.6, 1.0, 1.0],
    metallicFactor=0.0,
    roughnessFactor=0.2,
    alphaMode='OPAQUE'
)
mesh_pyrender = pyrender.Mesh.from_trimesh(
    mesh,
    smooth=True,
    wireframe=False,
    material=material
)

scene = pyrender.Scene(bg_color=[0, 0, 0, 255], ambient_light=np.array([0.2, 0.2, 0.2]))
scene.add(mesh_pyrender)

camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
cam_pose = np.eye(4)
cam_pose[2, 3] = extent
cam_node = scene.add(camera, pose=cam_pose)

fill_light = pyrender.DirectionalLight(color=np.ones(3), intensity=2.0)
fill_node = scene.add(fill_light, pose=cam_pose)

# side light
side_light = pyrender.DirectionalLight(color=np.ones(3), intensity=1.5)
side_pose = np.eye(4)
side_pose[:3, 3] = [extent, 0, 0] 
scene.add(side_light, pose=side_pose)

renderer = pyrender.OffscreenRenderer(viewport_width=512, viewport_height=512)
frames = []
elev = np.pi / 12.0

num_frames = 24

for i in range(num_frames):
    angle = 2 * np.pi * i / num_frames
    x = extent * np.cos(angle) * np.cos(elev)
    y = extent * np.sin(angle) * np.cos(elev)
    z = extent * np.sin(elev)

    pos = np.array([x, y, z])
    forward = -pos / np.linalg.norm(pos)
    world_up = np.array([0.0, 0.0, 1.0])
    right = np.cross(world_up, forward)
    right_norm = np.linalg.norm(right)
    if right_norm < 1e-8:
        right = np.array([1.0, 0.0, 0.0])
    else:
        right = right / right_norm
    up = np.cross(forward, right)

    cam_pose[:3, 0] = right
    cam_pose[:3, 1] = up
    cam_pose[:3, 2] = -forward 
    cam_pose[:3, 3] = pos

    scene.set_pose(cam_node, cam_pose)
    #scene.set_pose(light_node, cam_pose)

    angle_fill = angle + (np.pi / 3.0)
    xf = extent * np.cos(angle_fill) * np.cos(elev)
    yf = extent * np.sin(angle_fill) * np.cos(elev)
    zf = extent * np.sin(elev)
    pos_f = np.array([xf, yf, zf])
    forward_f = -pos_f / np.linalg.norm(pos_f)
    right_f = np.cross(world_up, forward_f)
    rn = np.linalg.norm(right_f)
    right_f = right_f if rn < 1e-8 else (right_f / rn)
    up_f = np.cross(forward_f, right_f)
    fill_pose = np.eye(4)
    fill_pose[:3, 0] = right_f
    fill_pose[:3, 1] = up_f
    fill_pose[:3, 2] = -forward_f
    fill_pose[:3, 3] = pos_f
    scene.set_pose(fill_node, fill_pose)

    color, _ = renderer.render(scene)
    frames.append(color[:, :, :3])

renderer.delete()
imageio.mimsave(outp, frames, fps=8, loop=0)