'''
The correctness should be guaranteed in the implementation itself.
This test only do debugging stuff and will always succeed.
'''

from model.config import *
from model.param import M

import unittest

class TestTasks(unittest.TestCase):
    def test_access(self):
        print("[Task] Access:")
        RAND.restore()
        print(ACCESS.genIOpairLen(M))
        print()
        pass

    def test_increment(self):
        print("[Task] Increment:")
        RAND.restore()
        print(INCREAMENT.genIOpairLen(M))
        print()
        pass



