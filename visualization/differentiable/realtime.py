import time

import trimesh
import pyrr
import pyrender
from pyrender import PerspectiveCamera, \
    DirectionalLight, SpotLight, PointLight, \
    MetallicRoughnessMaterial, \
    Primitive, Mesh, Node, Scene, \
    OffscreenRenderer, Viewer

import numpy as np
import cv2

from visualization.parametric.shapes import parametric_surface

if __name__ == '__main__':
    R = 10
    r = 3
    delta_r = 0.1
    off_screen_renderer = OffscreenRenderer(viewport_width=640 * 2, viewport_height=480 * 2)

    t = 0
    frame = 0
    start_time = time.time()
    direc_l = DirectionalLight(color=np.ones(3), intensity=1.0)
    spot_l = SpotLight(color=np.ones(3), intensity=10.0,
                       innerConeAngle=np.pi / 16, outerConeAngle=np.pi / 6)
    point_l = PointLight(color=np.ones(3), intensity=10.0)

    cam = PerspectiveCamera(yfov=(np.pi / 3.0))
    cam_pose = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 30.0],
        [0.0, 0.0, 0.0, 1.0],
    ])
    delta_r = 0.1
    while True:
        r += delta_r
        frame += 1
        t += 50
        if t % 1000 == 0:
            delta_r *= -1

        s = parametric_surface.doughnut(R, r, [50, 20])

        doughnut_trimesh = trimesh.Trimesh(vertices=s.flat_vertices, faces=s.flat_triangular_mesh_indices, )
        # for facet in doughnut_trimesh.facets:
        #     doughnut_trimesh.visual.face_colors[facet] = trimesh.visual.random_color()
        mesh = pyrender.Mesh.from_trimesh(doughnut_trimesh, smooth=False)
        mesh_node = Node(mesh=mesh, translation=np.array([0.0, 0.0, 0.0]))

        scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]), bg_color=[0.0, 0.0, 0.0])
        cam_node = scene.add(cam, pose=cam_pose)
        scene.add_node(mesh_node)
        # v = Viewer(scene)
        color, depth = off_screen_renderer.render(scene)
        cv2.imshow('f', color)
        cv2.waitKey(1)
        end_time = time.time()
        print(frame / (end_time - start_time))


    off_screen_renderer.delete()
