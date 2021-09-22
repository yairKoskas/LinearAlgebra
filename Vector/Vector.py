import math


class Vector:
    def __init__(self, *args):
        self.values = list(args)

    def __mul__(self, o):
        if isinstance(o, Vector):
            return sum([i * j for i, j in zip(self.values, o.values)])
        else:
            return Vector(*[o * i for i in self.values])

    def __truediv__(self, o):
        if isinstance(o, Vector):
            raise TypeError("Vector division isn't well defined")
        else:
            return Vector(*[i / o for i in self.values])

    def __add__(self, o):
        return Vector(*[i + j for i, j in zip(self.values, o.values)])

    def __sub__(self, o):
        return Vector(*[i - j for i, j in zip(self.values, o.values)])

    def __repr__(self):
        st = ''
        for i in self.values:
            st += f'{i}\n'
        return st

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __eq__(self, other):
        if isinstance(other, (float, int)):
            return self.values == [other for _ in range(len(self))]
        return self.values == other.values

    def size(self):
        return math.sqrt(sum([i ** 2 for i in self.values]))

    def __setitem__(self, key, value):
        self.values[key] = value

    @staticmethod
    def Ei(size, i):
        values = []
        for j in range(size):
            values.append(0 if i != j else 1)
        return Vector(*values)

    def append(self, param):
        self.values.append(param)


def gaussian_lattice_reduction(v1, v2):
    while True:
        if v2.size() < v1.size():
            v1, v2 = v2, v1
        m = math.floor((v1 * v2) / (v1 * v1))
        if m == 0:
            return v1, v2
        else:
            v2 = v2 - v1 * m


def gram_schmidt(basis, Normalize=True):
    vectors = [basis[0]]
    for i in range(1, len(basis)):
        mue = []
        for j in range(0, i):
            mue.append(float(basis[i] * vectors[j]) / (vectors[j].size() ** 2))
        sub_vectors = [vectors[j] * mue[j] for j in range(0, i)]
        vec = Vector(*[0 for _ in range(len(basis[0]))])
        for v in sub_vectors:
            vec += v
        vec = vec if not vec == 0 else Vector(*[0 for _ in range(len(basis[0]))])
        vectors.append(basis[i] - vec)
    if Normalize:
        for i in range(len(vectors)):
            vectors[i] = vectors[i] / (vectors[i].size() ** 2)
    return vectors
