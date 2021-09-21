from Vector import Vector


class Matrix:
    def __init__(self, args):
        if isinstance(args, list):
            for i in args:
                if not len(i) == len(args[0]):
                    raise ValueError("Vectors lengths aren't equal")
            self.vectors = args
        elif isinstance(args, int):
            vectors = []
            for i in range(args):
                vectors.append(Vector.Vector.Ei(args, i))
            self.vectors = vectors

    def __add__(self, m):
        new_vectors = [v + u for v, u in zip(self.vectors, m.vectors)]
        return Matrix(new_vectors)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            temp = other
            other = self.Identity(len(self))
            for i in range(len(self)):
                other[i][i] *= temp
        elif isinstance(other, Vector.Vector):
            if not len(self.vectors) == len(other):
                raise ValueError("Matrix and vector sizes aren't compatible")
            out = Vector.Vector()
            for row in self.rows():
                out.append(sum([row[i] * other[i] for i in range(len(row))]))
            return out
        elif isinstance(other, Matrix):
            if not len(self.vectors) == len(other.vectors[0]):
                raise ValueError("Matrices sizes aren't compatible")
            m = Matrix.Zero(len(self))
            for i in range(len(self)):
                for j in range(len(self[0])):
                    m[j][i] = sum([self[i][k] * other[k][j] for k in range(len(self))])
            return m
        else:
            raise TypeError(f'Matrix multiplication with {type(other)} isn\'t defined')

    def __pow__(self, power, modulo=None):
        if modulo:
            raise ValueError("Matrix modulo isn't well defined")
        m = Matrix.Identity(len(self))
        for i in range(power):
            m *= self
        return m

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.vectors[key]
        else:
            return Matrix(self.vectors[key.start:key.stop])

    def __setitem__(self, key, value):
        self.vectors[key] = value

    def is_square(self):
        return len(self.vectors) == len(self.vectors[0])

    def gauss_jordan_elimination(self):
        pass

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

    @staticmethod
    def Zero(length):
        vectors = []
        for i in range(length):
            vectors.append(Vector.Vector(*[0 for _ in range(length)]))
        return Matrix(vectors)

    def __repr__(self):
        s = ''
        for i in range(len(self.vectors[0])):
            s += ' '.join(str(v[i]) for v in self.vectors)
            s += '\n'
        return s

    @staticmethod
    def Identity(length):
        vectors = []
        for i in range(length):
            vectors.append(Vector.Vector.Ei(length, i))
        return Matrix(vectors)

    def __copy__(self):
        return Matrix(self.vectors)

    def trace(self):
        if self.is_square():
            return sum(self[i][i] for i in range(len(self)))

    def transpose(self):
        new_vectors = []
        for i in range(len(self.vectors[0])):
            new_vectors.append(Vector.Vector(*[v[i] for v in self.vectors]))
        return Matrix(new_vectors)

    def rows(self):
        return self.transpose().vectors
