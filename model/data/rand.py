'''
Manage the global random state
'''
from ..param import useSeed, randomSeed
from sys import maxsize
from random import randint, setstate, getstate, seed

class Rand:
    def __init__(self):
        seed(randomSeed if useSeed else randint(maxsize))
        self.__state = getstate()

    def restore(self):
        setstate(self.__state)

