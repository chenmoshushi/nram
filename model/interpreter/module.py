from ..config import M
from .datatype import DataType, Discrete, Fuzzy

import numpy as np
from abc import ABC, abstractmethod


class Module(ABC):
    '''
    Module are functions to be interpreted and executed
      has two inputs, and one output
      note the input type maybe discrete or fuzzy
    '''
    def __init__(self):
        pass

    def __call__(self, x: DataType, y: DataType) -> DataType:
        '''
        Case analysis on input type
        '''
        if isinstance(x, Discrete) and isinstance(y, Discrete):
            return self._discrete(x.v, y.v)
        elif isinstance(x, Fuzzy) and isinstance(y, Fuzzy):
            return self._fuzzy(x.v, y.v)
        else:
            raise TypeError('Module: inconsistent input data types')

    @abstractmethod
    def _discrete(self, vx, vy):
        raise NotImplementedError

    @abstractmethod
    def _fuzzy(self, vx, vy):
        raise NotImplementedError


class Zero(Module):

    def _discrete(self, vx, vy):
        return Discrete(0)

    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[0] = 1.0
        return Fuzzy(res)


class One(Module):

    def _discrete(self, vx, vy):
        return Discrete(1)

    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[1] = 1.0
        return Fuzzy(res)

class Two(Module):

    def _discrete(self, vx, vy):
        return Discrete(2)
    
    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[2] = 1.0
        return Fuzzy(res)


class Inc(Module):
    '''
    (vx + 1) modM
    '''
    def _discrete(self, vx, vy):
        return Discrete((vx + 1) % M)
    
    def _fuzzy(self, vx, vy):
        return Fuzzy(np.roll(vx, 1))


class Add(Module):

    def _discrete(self, vx, vy):
        return Discrete((vx + vy) % M)

    def _fuzzy(self, vx, vy):
        return Fuzzy(modM(np.convolve(vx, vy)))

class Sub(Module):

    def _discrete(self, vx, vy):
        return Discrete((vx - vy) % M)

    def _fuzzy(self, vx, vy):
        '''
        result[(i - j) % M] = vx[i] - vy[j]
        we can reverse the vy, convolve, then shift back to the 0 postion
        this is a valid implementation following (i + (M - j)) % M = (i - j) % M
        '''
        return Fuzzy(modM(np.roll(np.convolve(vx, vy[::-1]), -len(vy)+1)))

def modM(x: np.ndarray) -> np.ndarray:
    chunks = np.concatenate((x, np.zeros((M - len(x) % M) % M))).reshape(-1, M)
    return np.sum(chunks, axis=0)

