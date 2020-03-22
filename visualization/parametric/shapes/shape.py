class Shape:
    def __init__(self, parameters: dict, resolution: tuple):
        self.parameters = parameters
        self.resolution = resolution
        self.vertices = None

    def get_faces(self):
        """
        :return: n * m * 3 numpy array
        """

    def generate_quadratic_indices(self, closed=True):
        rows = []
        cols = []
        if closed:
            start = -1
        else:
            start = 0
        for i in range(start, self.resolution[0] - 1):
            for j in range(start, self.resolution[1] - 1):
                rows.append([i, i + 1, i + 1, i])
                cols.append([j, j, j + 1, j + 1])

        return rows, cols

    def generate_triangular_indices(self, closed=True):
        rows = []
        cols = []
        if closed:
            start = -1
        else:
            start = 0
        for i in range(start, self.resolution[0] - 1):
            for j in range(start, self.resolution[1] - 1):
                rows.append([i, i + 1, i + 1])
                cols.append([j, j, j + 1])
                rows.append([i, i + 1, i])
                cols.append([j, j + 1, j + 1])

        return rows, cols
