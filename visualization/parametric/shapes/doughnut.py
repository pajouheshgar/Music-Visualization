import numpy as np
from visualization.parametric.shapes.shape import Shape
from visualization.parametric.transformations.transformation import VertexTransformation


class Doughnut(Shape):
    def __init__(self, parameters):
        """

        :param parameters: a dict with keys
        R: inner radius of the donut
        r: width of the doughnut


        """
        super().__init__(parameters)
        self.R = self.parameters["R"]
        self.r = self.parameters["r"]
        self.vertex_transformations = []

    def add_transformation(self, transformation: VertexTransformation):
        self.vertex_transformations.append(transformation)
        return self

    def get_faces(self, resolution: tuple, triangular=False):
        R, r = self.R, self.r
        phis_resolution, thetas_resolution = resolution
        phis = np.linspace(0, 2 * np.pi, phis_resolution)
        thetas = np.linspace(0, 2 * np.pi, thetas_resolution)
        thetas_mesh, phis_mesh = np.meshgrid(thetas, phis)
        ro = R + r * np.cos(thetas_mesh)
        x = ro * np.cos(phis_mesh)
        y = ro * np.sin(phis_mesh)
        z = r * np.sin(thetas_mesh)
        vertices = np.stack([x, y, z], axis=-1)
        for transformation in self.vertex_transformations:
            vertices = transformation.transform(vertices)

        if not triangular:
            mesh_indices = Shape.generate_quadratic_indices(resolution)
        else:
            mesh_indices = Shape.generate_triangular_indices(resolution)
        return vertices[mesh_indices]


if __name__ == '__main__':
    D = Doughnut({"R": 5, "r": 2})
    faces = D.get_faces((50, 20))
    print(faces.shape)
    print(faces.shape)
