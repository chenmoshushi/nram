from model.interpreter.datatype import DataType, Discrete, Fuzzy
from model.interpreter.util import normalDisFuzzy
from model.config import mem, reg
from model.param import M, R

import unittest
import numpy as np

class TestMemory(unittest.TestCase):

    def setUp(self):
        self.d0 = Discrete(0)
        self.d1 = Discrete(1)
        self.d2 = Discrete(2)
        self.f0 = normalDisFuzzy([0])
        self.f1 = normalDisFuzzy([1])
        self.f2 = normalDisFuzzy([2])
        self.f12 = normalDisFuzzy([1, 2])
        self.f23 = normalDisFuzzy([2, 3])

    def test_clear_and_get(self):
        mem.clear()
        self.assertTrue(np.array_equal(mem.get(self.d0).v, self.f0.v))
        self.assertTrue(np.array_equal(mem.get(self.f0).v, self.f0.v))

    def test_set_and_get_one_point(self):
        mem.clear()
        mem.set(self.d0, self.d1)
        self.assertTrue(np.array_equal(mem.get(self.d0).v, self.f1.v))
        self.assertTrue(np.array_equal(mem.get(self.f0).v, self.f1.v))
        self.assertTrue(np.array_equal(mem.get(self.d1).v, self.f0.v))
        self.assertTrue(np.array_equal(mem.get(self.f1).v, self.f0.v))
        mem.set(self.f0, self.f2)
        self.assertTrue(np.array_equal(mem.get(self.d0).v, self.f2.v))
        self.assertTrue(np.array_equal(mem.get(self.f0).v, self.f2.v))
        self.assertTrue(np.array_equal(mem.get(self.d1).v, self.f0.v))
        self.assertTrue(np.array_equal(mem.get(self.f1).v, self.f0.v))

    def test_set_and_get_fuzzy_pointer(self):
        mem.clear()
        mem.set(self.f12, self.f1)
        self.assertTrue(np.array_equal(mem.get(self.f0).v, self.f0.v))
        self.assertTrue(np.array_equal(mem.get(self.f1).v, np.array([0.5, 0.5] + [0.0] * (M-2))))
        self.assertTrue(np.array_equal(mem.get(self.f2).v, np.array([0.5, 0.5] + [0.0] * (M-2))))

    def test_set_and_get_fuzzy_value(self):
        mem.clear()
        mem.set(self.f12, self.f12)
        self.assertTrue(np.array_equal(mem.get(self.f0).v, self.f0.v))
        self.assertTrue(np.array_equal(mem.get(self.f1).v, np.array([0.5, 0.25, 0.25] + [0.0] * (M-3))))
        self.assertTrue(np.array_equal(mem.get(self.f2).v, np.array([0.5, 0.25, 0.25] + [0.0] * (M-3))))

class test_register(unittest.TestCase):

    def setUp(self):
        self.f0 = normalDisFuzzy([0], R)
        self.f1 = normalDisFuzzy([1], R)
        self.f01 = normalDisFuzzy([0, 1])
        self.f12 = normalDisFuzzy([1, 2])

    def test_set_and_output(self):
        reg.clear()
        reg.set(self.f0, self.f01)
        reg.set(self.f1, self.f12)
        self.assertTrue(np.array_equal(reg.output(), np.array([0.5, 0.0] + [1.0] * (R-2))))

