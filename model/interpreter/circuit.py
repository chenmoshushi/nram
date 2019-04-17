'''
A circuit is a composition of modules
and is attached to a set of registers that is always initialized to zeros before execution
'''
from datatype import DataType, Discrete, Fuzzy
from ..config import regStack
from ..param import R

from collections import namedtuple

Layer = namedtuple('Layer', 'mod a b')

class Circuit:
    def __init__(self, reg):
        self._reg = reg
        self._wid = R
        # list of layers
        self._mods = []

    def cascade(self, mod, a, b):
        # add a module to current circuit, use a & b to control the fuzzy input
        self._mods.append(Layer(mod, a, b))



        


