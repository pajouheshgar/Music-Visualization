import numpy as np
from cached_property import cached_property
from visualization.parametric.transformations.transformation import VertexTransformation


class ParametricSurface:
    def __init__(self, vertices, closed=(True, True)):
        self.resolution = vertices.shape[:2]
        self.closed = closed
        self.vertices = vertices

    def get_faces(self, triangular=False):
        mesh_indices = self.quadratic_mesh_indices
        if triangular:
            mesh_indices = self.triangular_mesh_indices
        return self.vertices[mesh_indices]

    @cached_property
    def flat_vertices(self):
        return self.vertices.reshape([-1, 3])

    @cached_property
    def flat_triangular_mesh_indices(self):
        rows, cols = self.triangular_mesh_indices
        rows = np.array(rows).reshape([-1, 3])
        cols = np.array(cols).reshape([-1, 3])
        if self.closed[0]:
            rows[rows == -1] = self.resolution[0] - 1
        if self.closed[1]:
            cols[cols == -1] = self.resolution[1] - 1

        return rows * self.resolution[1] + cols

    @cached_property
    def flat_quadratic_mesh_indices(self):
        rows, cols = self.quadratic_mesh_indices
        rows = np.array(rows).reshape([-1, 4])
        cols = np.array(cols).reshape([-1, 4])

        if self.closed[0]:
            rows[rows == -1] = self.resolution[0] - 1
        if self.closed[1]:
            cols[cols == -1] = self.resolution[1] - 1

        return rows * self.resolution[1] + cols

    @cached_property
    def quadratic_mesh_indices(self):
        rows = []
        cols = []
        start = [0, 0]
        for i, p in enumerate(self.closed):
            if p:
                start[i] = -1

        for i in range(start[0], self.resolution[0] - 1):
            for j in range(start[1], self.resolution[1] - 1):
                rows.append([i, i + 1, i + 1, i])
                cols.append([j, j, j + 1, j + 1])

        return rows, cols

    @cached_property
    def triangular_mesh_indices(self):
        rows = []
        cols = []

        start = [0, 0]
        for i, p in enumerate(self.closed):
            if p:
                start[i] = -1

        for i in range(start[0], self.resolution[0] - 1):
            for j in range(start[1], self.resolution[1] - 1):
                rows.append([i, i + 1, i + 1])
                cols.append([j, j, j + 1])
                rows.append([i, i + 1, i])
                cols.append([j, j + 1, j + 1])

        return rows, cols

    def transform(self, transformation: VertexTransformation):
        self.vertices = transformation.transform(self.vertices)
        return self


def doughnut(R, r, resolution):
    phis_resolution, thetas_resolution = resolution
    phis = np.linspace(0, 2 * np.pi, phis_resolution, endpoint=False)
    thetas = np.linspace(0, 2 * np.pi, thetas_resolution, endpoint=False)
    thetas_mesh, phis_mesh = np.meshgrid(thetas, phis)
    ro = R + r * np.cos(thetas_mesh)
    x = ro * np.cos(phis_mesh)
    y = ro * np.sin(phis_mesh)
    z = r * np.sin(thetas_mesh)
    return ParametricSurface(np.stack([x, y, z], axis=-1), (True, True))
