from .datatype import DataType, Discrete, Fuzzy
from ..config import M

import numpy as np
from typing import List


def normalDisFuzzy(xs: List[int]) -> Fuzzy:
    p = 1.0 / len(xs)
    res = np.zeros(M)
    for x in xs:
        res[x] = p
    return Fuzzy(res)

