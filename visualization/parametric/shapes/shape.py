class Shape:
    def __init__(self, parameters):
        self.parameters = parameters

    def get_faces(self, resolution):
        """

        :param resolution: resolution of meshing
        :return: n * m * 3 numpy array
        """

    @staticmethod
    def generate_quadratic_indices(resolution, closed=True):
        rows = []
        cols = []
        if closed:
            start = -1
        else:
            start = 0
        for i in range(start, resolution[0] - 1):
            for j in range(start, resolution[1] - 1):
                rows.append([i, i + 1, i + 1, i])
                cols.append([j, j, j + 1, j + 1])

        return rows, cols

    @staticmethod
    def generate_triangular_indices(resolution, closed=True):
        rows = []
        cols = []
        if closed:
            start = -1
        else:
            start = 0
        for i in range(start, resolution[0] - 1):
            for j in range(start, resolution[1] - 1):
                rows.append([i, i + 1, i + 1])
                cols.append([j, j, j + 1])
                rows.append([i, i + 1, i])
                cols.append([j, j + 1, j + 1])

        return rows, cols


# class CompositeShape:
#     def
