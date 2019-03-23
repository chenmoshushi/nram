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


class Dec(Module):

    def _discrete(self, vx, vy):
        return Discrete((vx - 1) % M)

    def _fuzzy(self, vx, vy):
        return Fuzzy(np.roll(vx, -1))

class LessThan(Module):

    def _discrete(self, vx, vy):
        return Discrete(1 if vx < vy else 0)

    def _fuzzy(self, vx, vy):
        # probability of x >= y until the current index (x)
        ge = 0.0
        # probability of y <= the current index (x)
        acc = 0.0
        for x, y in zip(vx, vy):
            acc += y       # p(y <= index)
            ge += x * acc  # p(x == index and y <= index)
        res = np.zeros(M)
        res[0] = ge
        res[1] = 1.0 - ge
        return Fuzzy(res)


class LessEqual(Module):

    def _discrete(self, vx, vy):
        return Discrete(1 if vx <= vy else 0)

    def _fuzzy(self, vx, vy):
        # probability of x > y until the current index (x)
        gt = 0.0
        # probability of y < the current index (x)
        acc = 0.0
        for x, y in zip(vx, vy):
            gt += x * acc  # p(x == index and y < index)
            acc += y       # p(y <= index)
        res = np.zeros(M)
        res[0] = gt
        res[1] = 1.0 - gt
        return Fuzzy(res)


class Equal(Module):

    def _discrete(self, vx, vy):
        return Discrete(1 if vx == vy else 0)

    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        res[1] = np.inner(vx, vy)
        res[0] = 1.0 - res[1]
        return Fuzzy(res)


class Min(Module):

    def _discrete(self, vx, vy):
        return Discrete(min(vx, vy))

    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        accx = 1.0
        accy = 1.0
        for i, (x, y) in enumerate(zip(vx, vy)):
            # Inclusion–exclusion principle
            # eval to i when x == i && y >= i
            #             or y == i && x >= i
            # and we need to minus the overlap case of
            #                x == i && y == i
            res[i] = x * accy + y * accx - x * y
            accx -= x
            accy -= y
        return Fuzzy(res)


class Max(Module):

    def _discrete(self, vx, vy):
        return Discrete(max(vx, vy))

    def _fuzzy(self, vx, vy):
        res = np.zeros(M)
        accx = 0.0
        accy = 0.0
        for i, (x, y) in enumerate(zip(vx, vy)):
            # Inclusion–exclusion principle
            # eval to i when x == i && y <= i
            #             or y == i && x <= i
            # and we need to minus the overlap case of
            #                x == i && y == i
            res[i] = x * accy + y * accx - x * y
            accx += x
            accy += y
        return Fuzzy(res)


def modM(x: np.ndarray) -> np.ndarray:
    chunks = np.concatenate((x, np.zeros((M - len(x) % M) % M))).reshape(-1, M)
    return np.sum(chunks, axis=0)

