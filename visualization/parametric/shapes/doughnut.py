import numpy as np
from visualization.parametric.shapes.shape import Shape
from visualization.parametric.transformations.transformation import VertexTransformation


class Doughnut(Shape):
    def __init__(self, parameters, resolution):
        """

        :param parameters: a dict with keys
        :param resolution: rendering resolution of the shape
        R: inner radius of the donut
        r: width of the doughnut
        """
        super().__init__(parameters, resolution)
        self.R = self.parameters["R"]
        self.r = self.parameters["r"]
        self._generate_vertices_and_indices()

    def _generate_vertices_and_indices(self):
        R, r = self.R, self.r
        phis_resolution, thetas_resolution = self.resolution
        phis = np.linspace(0, 2 * np.pi, phis_resolution, endpoint=False)
        thetas = np.linspace(0, 2 * np.pi, thetas_resolution, endpoint=False)
        thetas_mesh, phis_mesh = np.meshgrid(thetas, phis)
        ro = R + r * np.cos(thetas_mesh)
        x = ro * np.cos(phis_mesh)
        y = ro * np.sin(phis_mesh)
        z = r * np.sin(thetas_mesh)
        self.vertices = np.stack([x, y, z], axis=-1)

        self.quadratic_mesh_indices = self.generate_quadratic_indices(True)
        self.triangular_mesh_indices = self.generate_triangular_indices(True)

    def add_transformation(self, transformation: VertexTransformation):
        self.vertices = transformation.transform(self.vertices)
        return self

    def get_faces(self, triangular=False):
        mesh_indices = self.quadratic_mesh_indices
        if triangular:
            mesh_indices = self.triangular_mesh_indices
        return self.vertices[mesh_indices]


if __name__ == '__main__':
    D = Doughnut({"R": 5, "r": 2}, (50, 20))
    faces = D.get_faces()
    print(faces.shape)
    print(faces.shape)
