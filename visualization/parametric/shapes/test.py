import os
import cv2
import pyrr
import cairosvg

import visualization.parametric.utils.svg3d as svg3d
from visualization.parametric.shapes.doughnut import Doughnut
from visualization.parametric.transformations.deformations import RandomNoise
from visualization.parametric.transformations.rotations import XRotation

import numpy as np

L = pyrr.vector.normalize(np.float32([0, 0, -1.0]))
H = pyrr.vector.normalize(np.float32([0.0, -1.0, -1.0]))

Shininess = 100.0


def frontface_shader(winding, face):
    if winding < 0:
        return None
    # face = faces[face_index]
    p0, p1, p2 = pyrr.Vector3(face[0]), pyrr.Vector3(face[1]), pyrr.Vector3(face[-1])
    N = pyrr.vector.normalize(pyrr.vector3.cross(p1 - p0, p2 - p0))
    df = max(0, np.dot(N, -L)) * 0.9
    sf = pow(max(0, np.dot(N, -H)), Shininess)
    # print(sf)
    color = df * np.float32([1, 1, 0]) + sf * np.float32([1, 1, 1])
    color = np.power(color, 1.0 / 2.2)
    return dict(
        fill=svg3d.rgb(*color), fill_opacity='1.0',
        stroke='black', stroke_width='0.001')


if __name__ == '__main__':
    view = pyrr.matrix44.create_look_at(
        eye=[0, 0, 120], target=[0, 0, 0], up=[0, 1, 0]
    )
    projection = pyrr.matrix44.create_perspective_projection(
        fovy=15, aspect=1, near=10, far=200
    )
    camera = svg3d.Camera(view, projection)

    style = dict(
        fill="white",
        fill_opacity="0.75",
        stroke="black",
        stroke_linejoin="round",
        stroke_width="0.001",
    )

    alpha = 0
    while True:
        alpha += 3
        faces = Doughnut({"R": 8, "r": 5}).add_transformation(RandomNoise({"distortion": 0.05})).add_transformation(
            XRotation({"angle": alpha})).get_faces(resolution=(50, 30), triangular=False)

        print(faces.shape)
        mesh = svg3d.Mesh(faces, shader=frontface_shader)
        view = svg3d.View(camera, svg3d.Scene([mesh]))
        svg3d.Engine([view]).render("temp.svg")
        cairosvg.svg2png(url="temp.svg", write_to="temp.png")
        image = cv2.imread("temp.png")
        os.remove("temp.svg")
        os.remove("temp.png")
        cv2.imshow("test", image)
        cv2.waitKey(1)
