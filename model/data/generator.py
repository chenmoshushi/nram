'''
Generator style data
I/O pairs & trace
'''
from ..param import M, NULL

import numpy as np
from abc import ABC, abstractmethod
from random import randint, shuffle
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
    def _genIn(self, n: int) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def _genOut(self, i, trace: bool) -> List[int]:
        raise NotImplementedError


class Access(DataGen):
    '''
    input  : k : A[0] : A[1] : ... : A[n-1] : NULL
    output : A[k] : A[0] : A[1] : ... : A[n-1] : NULL
    '''
    def _lenToN(self, length):
        return length - 2

    def _genIn(self, n):
        arr = self._genArray(n)
        k = randint(0, n-1)
        return [k] + arr + [NULL]
        
    def _genOut(self, i, trace):
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
    def _lenToN(self, length):
        return length - 1

    def _genIn(self, n):
        arr = self._genArray(n)
        return arr + [NULL]

    def _genOut(self, i, trace):
        o = [x+1 if x != NULL else x for x in i] 
        if trace:
            raise NotImplementedError
        else:
            return o

class Copy(DataGen):
    '''
    input  : p : A[0] : A[1] : ... : A[n-1] (p >= n+1) <- non overlapping
    output : copy the array to where p start
    '''
    def _lenToN(self, length):
        return randint(1, length // 3 - 1)

    def _genIn(self, n):
        arr = self._genArray(n)
        p = n + randint(1, n)
        return [p] + arr

    def _genOut(self, i, trace):
        offset = i[0] - len(i)
        o = i + [NULL] * offset + i
        if trace:
            raise NotImplementedError
        else:
            return o

class Reverse(DataGen):
    '''
    input  : p : A[0] : A[1] : ... : A[n-1] (p >= n+1) <- non overlapping
    output : copy the reversed array to where p start
    '''
    def _lenToN(self, length):
        return randint(1, length // 3 - 1)

    def _genIn(self, n):
        arr = self._genArray(n)
        p = n + randint(1, n)
        return [p] + arr

    def _genOut(self, i, trace):
        offset = i[0] - len[i]
        o = i + [NULL] * offset + reversed(i)
        if trace:
            raise NotImplementedError
        else:
            return o

class Swap(DataGen):
    '''
    input  : p : q : A[0] : A[1] : ... : A[p] : ... A[q] : ... : A[n-1]
    output : p : q : A[0] : A[1] : ... : A[q] : ... A[p] : ... : A[n-1]
    '''
    def _lenToN(self, length):
        return length - 2

    def _genIn(self, n):
        arr = self._genArray(n)
        p = randint(0, n-1)
        q = randint(0, n-1)
        return [p, q] + arr

    def _genOut(self, i, trace):
        o = i[:]
        realp = o[0]+2
        realq = o[1]+2
        temp = o[realp]
        o[realp] = o[realq]
        o[realq] = temp
        if trace:
            raise NotImplementedError
        else:
            return o

class Permutation(DataGen):
    '''
    input  : P[0] : P[1] : ... : P[n-1] : A[0] : A[1] : ... A[n-1]
             P is a permutation of [0..n-1]
    output : A is permutated according to P
    '''
    def _lenToN(self, length):
        return length // 2

    def _genIn(self, n):
        p = range(n)
        shuffle(p)
        arr = self._genArray(n)
        return p + arr

    def _genOut(self, i, trace):
        half = len(i) // 2
        p, a = i[:half], i[half:]
        oa = [0] * half
        for k in range(half):
            oa[p[k]] = a[k]
        o = p + oa
        if trace:
            raise NotImplementedError
        else:
            return o

