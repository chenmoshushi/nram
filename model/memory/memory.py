from ..param import M, NULL
from ..interpreter.datatype import DataType, Discrete, Fuzzy
from ..interpreter.util import castToFuzzy, fuzzyFromInt

import numpy as np
from typing import List

class Memory:
    def __init__(self):
        self._mem = np.zeros((M, M))
        self._mem[:,NULL] = 1.0

    def clear(self):
        self._mem = np.zeros((M, M))
        self._mem[:,NULL] = 1.0

    def initializeWith(self, xs: List[int]):
        if len(xs) > M:
            raise ValueError("initial value sequence is too long to fit in the memory")
        for (i, x) in enumerate(xs):
            self._mem[i] = fuzzyFromInt(x)

    def set(self, p: DataType, a: DataType):
        if isinstance(p, Discrete):
            self._mem[p.v] = castToFuzzy(a).v
        elif isinstance(p, Fuzzy):
            pointer = p.v.reshape((M, 1))
            value = castToFuzzy(a).v.reshape((M, 1))
            J = np.ones((M, 1))
            self._mem = np.multiply(np.matmul(J - pointer, np.transpose(J)), self._mem) + \
                        np.matmul(pointer, np.transpose(value))
        else:
            raise TypeError
    
    def get(self, p: DataType) -> Fuzzy:
        if isinstance(p, Discrete):
            return Fuzzy(self._mem[p.v])
        elif isinstance(p, Fuzzy):
            return Fuzzy(np.matmul(np.transpose(self._mem), p.v))
        else:
            raise TypeError

