from __future__ import annotations

from typing import Tuple, Union, Dict
import numpy as np


class Polynomial:
    def __init__(self, powers: Tuple[int, ...], coefficients: Tuple[Union[float, int], ...]):
        if len(set(powers)) != len(powers):
            raise ValueError("Duplicate powers")
        if len(powers) != len(coefficients):
            raise ValueError("Invalid number of powers and coefficients")
        self.powers = powers
        self.coefficients = coefficients
        self.power_coefficient_dict = dict(zip(self.powers, self.coefficients))
        self.polynomial = lambda x: sum([c * (x ** p) for p, c in zip(self.powers, self.coefficients)])

    def __add__(self, other: Polynomial):
        if set(other.coefficients) == {0}:
            return self

        s = self.power_coefficient_dict
        o = other.power_coefficient_dict
        #  Adding values with equal keys
        new_polynomial_power_coefficient_dict: Dict[int, float] = dict(list(s.items()) + list(o.items()) +
                                                                       [(k, s[k] + o[k]) for k in set(s) & set(o)])

        return Polynomial(tuple(new_polynomial_power_coefficient_dict.keys()),
                          tuple(new_polynomial_power_coefficient_dict.values()))

    def __sub__(self, other: Polynomial):
        return self + (-other)

    def __mul__(self, other: Polynomial):
        p = Polynomial((0,), (0,))

        r1 = max(self.powers) if isinstance(self.powers, tuple) else self.powers
        r2 = max(other.powers) if isinstance(other.powers, tuple) else other.powers

        # Using general Polynomial multiplication formula
        for i in range(r1 + r2 + 1):
            for j in range(i + 1):
                p = self.power_coefficient_dict.get(j, 0)
                q = other.power_coefficient_dict.get(i - j, 0)
                p += Polynomial((i,), (p * q,))
        return p

    def __neg__(self):
        return self * Polynomial((0,), (-1,))

    def __eq__(self, other):
        p1 = {k: v for k, v in self.power_coefficient_dict.items() if v != 0}
        p2 = {k: v for k, v in other.power_coefficient_dict.items() if v != 0}

        return p1 == p2

    def __copy__(self):
        return Polynomial(self.powers, self.coefficients)

    def __str__(self):
        chunks = []
        self.power_coefficient_dict = {k: v for k, v in sorted(self.power_coefficient_dict.items(),
                                                               key=lambda item: item[0])}
        for power in self.powers:
            coeff = self.power_coefficient_dict[power]
            if coeff == 0:
                continue
            chunks.append(str(coeff) if coeff < 0 else f"+{coeff}")
            chunks.append(f"x^{power}" if power != 0 else '')
        chunks[0] = chunks[0].lstrip("+")
        return ''.join(chunks).replace("+", " + ").replace("-", " - ")

    def roots(self):
        if len(self.power_coefficient_dict) == 1:
            return 0,
        coeffs = []
        m = max(self.powers) if isinstance(self.powers, tuple) else self.powers
        for i in range(m + 1):
            if i in self.powers:
                coeffs.append(self.power_coefficient_dict[i])
            else:
                coeffs.append(0)
        # using numpy to find roots for the polynomial
        zeros = np.roots(coeffs)
        if 0 not in self.power_coefficient_dict or self.power_coefficient_dict[0] == 0:
            zeros = list(zeros) + [0]
        return tuple(zeros)
