import pyrr
import numpy as np
from visualization.parametric.transformations.transformation import VertexTransformation


class ZRotation(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        angle: rotation amount in degrees
        """
        super().__init__(parameters)
        self.angle = parameters["angle"]

    def transform(self, vertices):
        R = pyrr.Matrix33.from_z_rotation(self.angle * np.pi / 180.0)
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_faces = (np.matmul(vertices, R)).reshape([n, m, d])
        return transformed_faces


class XRotation(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        angle: rotation amount in degrees
        """
        super().__init__(parameters)
        self.angle = parameters["angle"]

    def transform(self, vertices):
        R = pyrr.Matrix33.from_x_rotation(self.angle * np.pi / 180.0)
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_faces = (np.matmul(vertices, R)).reshape([n, m, d])
        return transformed_faces


class YRotation(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        angle: rotation amount in degrees
        """
        super().__init__(parameters)
        self.angle = parameters["angle"]

    def transform(self, vertices):
        R = pyrr.Matrix33.from_y_rotation(self.angle * np.pi / 180.0)
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_faces = (np.matmul(vertices, R)).reshape([n, m, d])
        return transformed_faces
