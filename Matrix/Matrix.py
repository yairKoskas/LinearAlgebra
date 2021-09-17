from Vector import Vector


class Matrix:
    def __init__(self, vectors):
        for i in vectors:
            if not len(i) == len(vectors[0]):
                raise ValueError("Vectors lengths aren't equal")
        self.vectors = vectors

    def __add__(self, m):
        new_vectors = [v + u for v, u in zip(self.vectors, m.vectors)]
        return Matrix(new_vectors)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.vectors[key]
        else:
            return Matrix(self.vectors[key.start:key.stop])

    def __setitem__(self, key, value):
        self.vectors[key] = value

    def is_square(self):
        return len(self.vectors) == len(self.vectors[0])

    def determinant(self):
        if not self.is_square():
            raise RuntimeError("Matrix isn't square!")

        indices = list(range(len(self)))
        det = 0
        if len(self) == 2:
            return self[0][0] * self[1][1] - self[1][0] * self[0][1]

        for fc in indices:
            As = Matrix(self.vectors)
            As = As[1:]
            height = len(As)
            for i in range(height):
                As[i] = As[i][0:fc] + As[i][fc + 1:]
            sign = (-1) ** (fc % 2)
            sub_det = As.determinant()
            det += self[0][fc] * sign * sub_det

        return det

    def __len__(self):
        return len(self.vectors)

    def __repr__(self):
        s = ''
        for i in range(len(self.vectors[0])):
            s += ' '.join(str(v[i]) for v in self.vectors)
            s += '\n'
        return s
