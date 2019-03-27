import numpy as np

class DataType(object):
    '''
    Input and output datatype
    may be discrete(a number between 0 to M-1) or fuzzy (distribution over 0 to M-1)
    '''
    def __init__(self, v):
        raise NotImplementedError
    
class Discrete(DataType):
    def __init__(self, v: int):
        if not isinstance(v, int):
            raise TypeError
        self.v = v

class Fuzzy(DataType):
    def __init__(self, v: np.ndarray):
        if not isinstance(v, np.ndarray):
            raise TypeError
        self.v = v

