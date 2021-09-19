import hashlib
from typing import Union
from random import randint
from Crypto.Util.number import inverse


class PointNotOnCurveError(Exception):
    def __init__(self, message="Point isn't on curve"):
        self.message = message
        super().__init__(self.message)


class EllipticCurve:
    def __init__(self, a: int, b: int, p=None):
        self.a = a
        self.b = b
        self.p = p

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.p == other.p


class EPoint:
    def __init__(self, x: Union[int, str], y: Union[int, str], ecurve: EllipticCurve):
        if ecurve.p:
            if isinstance(x, int):
                if not ((x ** 3 + ecurve.a * x + ecurve.b) % ecurve.p == (y ** 2) % ecurve.p):
                    raise PointNotOnCurveError()
                self.x = x % ecurve.p
                self.y = y % ecurve.p
            else:
                self.x = x
                self.y = y
        else:
            if isinstance(x, int):
                if not (x ** 3 + ecurve.a * x + ecurve.b == y ** 2):
                    raise PointNotOnCurveError()
            self.x = x
            self.y = y
        self.ecurve = ecurve

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.ecurve == other.ecurve

    def __add__(self, other):
        if self.x == 'o':
            return other
        elif other.x == 'o':
            return self
        x1, x2, y1, y2, a, p = self.x, other.x, self.y, other.y, self.ecurve.a, self.ecurve.p
        if x1 == x2 and y1 == -y2:
            return EPoint('o', 'o', self.ecurve)
        else:
            if self == other:
                l = ((3 * (x1 ** 2) + a) * inverse(2 * y1, p)) % p
            else:
                l = ((y2 - y1) * inverse((x2 - x1), p)) % p
            x3 = l ** 2 - x1 - x2
            y3 = l * (x1 - x3) - y1
            return EPoint(x3, y3, self.ecurve)

    def __mul__(self, n):
        q = self.__copy__()
        r = EPoint('o', 'o', q.ecurve)
        while n > 0:
            if n % 2 == 1:
                r = r + q
            q, n = q + q, int(n/2)
        return r

    def __repr__(self):
        return f'(x: {self.x}, y: {self.y})'

    def __copy__(self):
        return EPoint(**{'x': self.x, 'y': self.y, 'ecurve': self.ecurve})


e = EllipticCurve(2, 3, 5)
p = EPoint(0, 1, e)
