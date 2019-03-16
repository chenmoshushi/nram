from model.interpreter.datatype import DataType, Discrete, Fuzzy
from model.interpreter.util import normalDisFuzzy
from model.config import *

import unittest
from typing import List
import numpy as np


class TestModule(unittest.TestCase):

    def setUp(self):
        self.d0 = Discrete(42)
        self.d1 = Discrete(7)
        self.f0 = normalDisFuzzy([0])
        self.f1 = normalDisFuzzy([1])
        self.f2 = normalDisFuzzy([2])
        self.f12 = normalDisFuzzy([1, 2])
        self.f23 = normalDisFuzzy([2, 3])

    def test_correctType(self):
        with self.assertRaises(TypeError):
            ADD(self.d0, 1)
        with self.assertRaises(TypeError):
            ADD(self.d1, self.f0)

    def test_ZERO(self):
        self.assertEqual(ZERO(self.d0, self.d1).v, 0)
        self.assertTrue(np.array_equal(ZERO(self.f0, self.f12).v, self.f0.v))

    def test_ONE(self):
        self.assertEqual(ONE(self.d0, self.d1).v, 1)
        self.assertTrue(np.array_equal(ONE(self.f0, self.f12).v, self.f1.v))

    def test_TWO(self):
        self.assertEqual(TWO(self.d0, self.d1).v, 2)
        self.assertTrue(np.array_equal(TWO(self.f0, self.f12).v, self.f2.v))

    def test_INC(self):
        self.assertEqual(INC(self.d0, self.d1).v, 43)
        self.assertTrue(np.array_equal(INC(self.f0, self.f12).v, self.f1.v))
        self.assertTrue(np.array_equal(INC(self.f12, self.f2).v, self.f23.v))

    def test_ADD(self):
        self.assertEqual(ADD(self.d0, self.d1).v, 49)
        self.assertTrue(np.array_equal(ADD(self.f0, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(ADD(self.f12, self.f1).v, self.f23.v))

