# global memory instance
from .memory.memory import Memory
mem = Memory()

# global register instances
from .memory.memory import RegStack
regStack = RegStack()

# global module instances
from .interpreter.module import *

ZERO = Zero()
ONE = One()
TWO = Two()
INC = Inc()
ADD = Add()
SUB = Sub()
DEC = Dec()
LT = LessThan()
LE = LessEqual()
EQ = Equal()
MIN = Min()
MAX = Max()

# global random state management
from .data.rand import Rand
RAND = Rand()

# global data generator instances
from .data.generator import *

ACCESS = Access()
INCREAMENT = Increment()

