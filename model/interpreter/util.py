from .datatype import DataType, Discrete, Fuzzy
from ..param import M

import numpy as np
from typing import List


def normalDisFuzzy(xs: List[int]) -> Fuzzy:
    p = 1.0 / len(xs)
    res = np.zeros(M)
    for x in xs:
        res[x] = p
    return Fuzzy(res)

def fuzzyFromInt(a: int) -> Fuzzy:
    fuzz = np.zeros(M)
    fuzz[a] = 1.0
    return Fuzzy(fuzz)

def fuzzyFromDiscrete(a: Discrete) -> Fuzzy:
    return fuzzyFromInt(a.v)

def castToFuzzy(a: DataType) -> Fuzzy:
    return a if isinstance(a, Fuzzy) else fuzzyFromInt(a.v)

