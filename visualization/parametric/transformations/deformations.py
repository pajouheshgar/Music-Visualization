import pyrr
import numpy as np
from visualization.parametric.transformations.transformation import VertexTransformation


class RandomNoise(VertexTransformation):
    def __init__(self, parameters):
        """
        :param parameters: a dict with keys
        distortion: maximum amount of distortion
        """
        super().__init__(parameters)
        self.distortion = parameters["distortion"]

    def transform(self, vertices):
        n, m, d = vertices.shape
        noise = np.random.randn(n, m, d) * self.distortion
        return vertices + noise
