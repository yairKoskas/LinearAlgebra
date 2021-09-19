from Matrix import Matrix
from Vector import Vector


class Polynomial:
    def __init__(self, *args):
        self.coefficients = list(args)

    def eval(self, val):
        if not isinstance(val, Matrix.Matrix):
            return sum(self.coefficients[i] * (val ** i) for i in range(len(self.coefficients)))
        else:
            m = Matrix.Matrix.Identity(len(val)) * self.coefficients[0]
            for i in range(1, len(self.coefficients)):
                m = m + (val ** i) * self.coefficients[i]
            return m

    def __repr__(self):
        s = str(self.coefficients[0])
        for i in range(1, len(self.coefficients)):
            if i == 1:
                if self.coefficients[i] == 0:
                    pass
                elif self.coefficients[i] == 1:
                    s += f' + x'
                elif self.coefficients[i] == -1:
                    s += f' - x'
                elif self.coefficients[i] > 0:
                    s += f' + {self.coefficients[i]}x'
                else:
                    s += f' - {-self.coefficients[i]}x'
            else:
                if self.coefficients[i] == 0:
                    pass
                elif self.coefficients[i] == 1:
                    s += f' + x^{i + 1}'
                elif self.coefficients[i] == -1:
                    s += f' - x^{i + 1}'
                elif self.coefficients[i] > 0:
                    s += f' + {self.coefficients[i]}x^{i}'
                else:
                    s += f' - {-self.coefficients[i]}x^{i}'
        return s


def main():
    v1 = Vector.Vector(1, 2, 3)
    v2 = Vector.Vector(4, 5, 6)
    v3 = Vector.Vector(7, 8, 9)
    m = Matrix.Matrix([v1, v2, v3])
    print(m)
    print(m.transpose())
    a = Polynomial(1, 2, 3)
    print(a.eval(m))
    # print(a)
    # print(a.eval(m))


if __name__ == '__main__':
    main()
