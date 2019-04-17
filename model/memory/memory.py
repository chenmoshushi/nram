from ..param import M, R, NULL
from ..interpreter.datatype import DataType, Discrete, Fuzzy
from ..interpreter.util import castToFuzzy, fuzzyFromInt

import numpy as np
from typing import List

class Memory:
    def __init__(self):
        self._dim = M
        self.clear()

    def clear(self):
        self._mem = np.zeros((self._dim, M))
        self._mem[:,NULL] = 1.0
        self._mem[:,NULL] = 1.0

    def initializeWith(self, xs: List[int]):
        if len(xs) > self._dim:
            raise ValueError("initial value sequence is too long to fit in the memory")
        for (i, x) in enumerate(xs):
            self._mem[i] = fuzzyFromInt(x)

    def content(self):
        return self._mem

    def set(self, p: DataType, a: DataType):
        if isinstance(p, Discrete):
            self._mem[p.v] = castToFuzzy(a).v
        elif isinstance(p, Fuzzy):
            pointer = p.v.reshape((self._dim, 1))
            value = castToFuzzy(a).v.reshape((M, 1))
            Jp = np.ones((self._dim, 1))
            Jm = np.ones((M, 1))
            self._mem = np.multiply(np.matmul(Jp - pointer, np.transpose(Jm)), self._mem) + \
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


class Register(Memory):
    '''
    A register is a memory that has R dimensions
    and an output method to the controller
    '''
    def __init__(self):
        self._dim = R
        self.clear()

    def output(self):
        # output to controller, the probability of a register is zero
        return self._mem[:,NULL]

    def update(self, vals):
        # vals.shape needs to be (R, M)
        self._mem = vals



class RegStack:
    def __init__(self):
        self._stack = []

    def push(self):
        self._stack.append(Register())

    def top(self):
        return self._stack[-1]

    def pop(self):
        self._stack.pop()

