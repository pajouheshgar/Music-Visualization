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
        self.R = np.array(pyrr.Matrix33.from_z_rotation(self.angle * np.pi / 180.0))

    def transform(self, vertices):
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_vertices = (np.matmul(vertices, self.R)).reshape([n, m, d])
        return transformed_vertices


class XRotation(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        angle: rotation amount in degrees
        """
        super().__init__(parameters)
        self.angle = parameters["angle"]
        self.R = np.array(pyrr.Matrix33.from_x_rotation(self.angle * np.pi / 180.0))

    def transform(self, vertices):
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_vertices = (np.matmul(vertices, self.R)).reshape([n, m, d])
        return transformed_vertices


class YRotation(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        angle: rotation amount in degrees
        """
        super().__init__(parameters)
        self.angle = parameters["angle"]
        self.R = np.array(pyrr.Matrix33.from_y_rotation(self.angle * np.pi / 180.0))

    def transform(self, vertices):
        n, m, d = vertices.shape
        vertices = vertices.reshape(-1, d)
        transformed_vertices = (np.matmul(vertices, self.R)).reshape([n, m, d])
        return transformed_vertices
