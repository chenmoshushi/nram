'''
Generator style data
I/O pairs & trace
'''
from ..param import M, NULL

import numpy as np
from abc import ABC, abstractmethod
from random import randint, setstate
from typing import List

class DataGen(ABC):
    
    def genIOpairN(self, n: int, trace: bool=False):
        # n indicates the difficulty, the i/o sequence may exceed n
        i = self._genIn(n)
        ot = self._genOut(i, trace=trace)
        return (i,) + ot if isinstance(ot, tuple) else (i, ot)

    def genIOpairLen(self, length: int, trace: bool=False):
        # generate i/o sequence within the bound of length
        n = self._lenToN(length)
        return self.genIOpairN(n, trace)


    def _genArray(self, arrLength: int):
        return [randint(1, M) for i in range(arrLength)]

    @abstractmethod
    def _lenToN(self, length: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def _genIn(self, n: int):
        raise NotImplementedError

    @abstractmethod
    def _genOut(self, i, trace: bool):
        raise NotImplementedError


class Access(DataGen):
    '''
    input  : k : A[0] : A[1] : ... : A[n-1] : NULL
    output : A[k] : A[0] : A[1] : ... : A[n-1] : NULL
    '''
    def _lenToN(self, length: int) -> int:
        return length - 2

    def _genIn(self, n: int) -> List[int]:
        arr = self._genArray(n)
        k = randint(0, n-1)
        return [k] + arr + [NULL]
        
    def _genOut(self, i, trace: bool):
        o = [i[i[0]+1]] + i[1:]
        if trace:
            raise NotImplementedError
        else:
            return o

class Increment(DataGen):
    '''
    input  : A[0] : A[1] : ... A[n-1] : NULL
    output : A[0]+1 : A[1]+1 : ... A[n-1]+1 : NULL
    '''
    def _lenToN(self, length: int) -> int:
        return length - 1

    def _genIn(self, n: int) -> List[int]:
        arr = self._genArray(n)
        return arr + [NULL]

    def _genOut(self, i, trace: bool):
        o = [x+1 if x != NULL else x for x in i] 
        if trace:
            raise NotImplementedError
        else:
            return o

class Copy:
    '''
    input  : A[0]
    '''
