from ..config import M
from .datatype import DataType, Discrete, Fuzzy

import numpy as np

class Module(object):
    '''
    Module are functions to be interpreted and executed
      has two inputs, and one output
      note the input type maybe discrete or fuzzy
    '''
    def __init__(self):
        pass

    def __apply__(self, x: DataType, y: DataType) -> DataType:
        '''
        Case analysis on input type
        '''
        if isinstance(x, Discrete) and isinstance(y, Discrete):
            return self.__discrete(x.v, y.v)
        elif isinstance(x, Fuzzy) and isinstance(y, Fuzzy):
            return self.__fuzzy(x.v, y.v)
        else:
            raise TypeError('Module: inconsistent input data types')

    def __discrete(self):
        raise NotImplementedError

    def __fuzzy(self):
        raise NotImplementedError


class Zero(Module):
    def __discrete(self, vx, vy):
        return Discrete(0)

    def __fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[0] = 1.0
        return Fuzzy(res)


class One(Module):
    def __discrete(self, vx, vy):
        return Discrete(1)

    def __fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[1] = 1.0
        return Fuzzy(res)


class Add(Module):
    def __discrete(self, vx, vy):
        return Discrete(vx + vy)

    def __fuzzy(self, vx, vy):
        return Fuzzy(vx + vy)

