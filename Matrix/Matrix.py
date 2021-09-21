import math
from typing import List, Union

from Vector import Vector


class Matrix:
    def __init__(self, args: Union[List[Vector.Vector], int]):
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
        if all(isinstance(u, Vector.Vector) and isinstance(v, Vector.Vector) for u, v in zip(m.vectors, self.vectors)):
            new_vectors = [v + u for v, u in zip(self.vectors, m.vectors)]
            return Matrix(new_vectors)
        raise TypeError("Vector isn't the right type")

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            temp = self.__copy__()
            for i in range(len(temp)):
                for j in range(len(temp[0])):
                    temp[i][j] *= other
            return temp
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
        m = self.__copy__()
        for curr_vec in range(len(m)):
            if m[curr_vec] == 0:
                continue
            else:
                try:
                    # in case all values are 0
                    pivot = min([i for i in range(len(m[curr_vec])) if m[curr_vec][i] != 0 and i >= curr_vec])
                except ValueError:
                    continue
                m.swap_rows(curr_vec, pivot)
                m.mult_row(curr_vec, 1 / m[curr_vec][curr_vec])
                for i in range(0, len(self.vectors[0])):
                    if curr_vec == i:
                        continue
                    m.add_rows(curr_vec, i, -m[curr_vec][i])
        return m

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
        return Matrix(list(v.__copy__() for v in self.vectors))

    def trace(self):
        if self.is_square():
            return sum(self[i][i] for i in range(len(self)))

    def transpose(self):
        new_vectors = []
        for i in range(len(self.vectors[0])):
            new_vectors.append(Vector.Vector(*[v[i] for v in self.vectors]))
        return Matrix(new_vectors)

    def rows(self):
        return [Vector.Vector(*[v[i] for v in self.vectors]) for i in range(len(self.vectors[0]))]

    def swap_rows(self, curr_vec, pivot):
        for v in self.vectors:
            v[curr_vec], v[pivot] = v[pivot], v[curr_vec]

    def mult_row(self, row: int, value: float):  # What is this?
        for v in self.vectors:
            v[row] *= value
            if int(v[row]) == math.ceil(v[row]):
                v[row] = int(v[row])

    def add_rows(self, row1: int, row2: int, alpha: float = 1):
        for v in self.vectors:
            v[row2] += v[row1] * alpha
            if int(v[row2]) == math.ceil(v[row2]):
                v[row2] = int(v[row2])

    def solve(self, vec: Vector):
        solution = []
        if self.is_square() and self.determinant() != 0:
            # solve by kramer's rule
            det = self.determinant()
            for i in range(len(self)):
                m = self.__copy__()
                m.vectors[i] = vec
                solution.append(m.determinant() / det)
        else:
            vectors = list(self.vectors)
            vectors.append(vec)
            m = Matrix(vectors).gauss_jordan_elimination()
            for row in m.rows():
                # if there's a zeroed out row with non-zero value in the solution vector
                if row[:-1].count(0) == len(row[:-1]) and row[-1] != 0:
                    return None
            # there's a solution or infinite ones
            for row in m.rows():
                if row == 0:
                    solution.append(0)  # just for an example solution
                else:
                    solution.append(row[-1])
        return solution

    def inverse(self):
        if self.determinant() == 0:
            raise ValueError("Matrix isn't invertible")
        temp = Matrix(self.vectors + Matrix.Identity(len(self.vectors)).vectors)
        temp = temp.gauss_jordan_elimination()
        return Matrix(temp.vectors[len(self.vectors):])
