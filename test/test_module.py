from model.interpreter.datatype import DataType, Discrete, Fuzzy
from model.interpreter.util import normalDisFuzzy
from model.config import *
from model.param import M

import unittest
from typing import List
import numpy as np


class TestModule(unittest.TestCase):

    def setUp(self):
        self.d0 = Discrete(3)
        self.d1 = Discrete(4)
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
        self.assertEqual(INC(self.d0, self.d1).v, self.d0.v + 1)
        self.assertTrue(np.array_equal(INC(self.f0, self.f12).v, self.f1.v))
        self.assertTrue(np.array_equal(INC(self.f12, self.f2).v, self.f23.v))

    def test_ADD(self):
        self.assertEqual(ADD(self.d0, self.d1).v, self.d0.v + self.d1.v)
        self.assertTrue(np.array_equal(ADD(self.f0, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(ADD(self.f12, self.f1).v, self.f23.v))

    def test_SUB(self):
        self.assertEqual(SUB(self.d1, self.d0).v, self.d1.v - self.d0.v)
        self.assertTrue(np.array_equal(SUB(self.f2, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(SUB(self.f23, self.f1).v, self.f12.v))

    def test_DEC(self):
        self.assertEqual(DEC(self.d0, self.d1).v, self.d0.v - 1)
        self.assertEqual(DEC(self.d1, self.d1).v, self.d1.v - 1)
        self.assertTrue(np.array_equal(DEC(self.f2, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(DEC(self.f1, self.f12).v, self.f0.v))
        self.assertTrue(np.array_equal(DEC(self.f23, self.f0).v, self.f12.v))

    def test_LT(self):
        self.assertEqual(LT(self.d0, self.d1).v, 1)
        self.assertEqual(LT(self.d1, self.d1).v, 0)
        self.assertEqual(LT(self.d1, self.d0).v, 0)
        self.assertTrue(np.array_equal(LT(self.f0, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(LT(self.f1, self.f1).v, self.f0.v))
        self.assertTrue(np.array_equal(LT(self.f23, self.f23).v, np.array([0.75, 0.25] + [0.0] * (M-2))))

    def test_LE(self):
        self.assertEqual(LE(self.d0, self.d1).v, 1)
        self.assertEqual(LE(self.d1, self.d1).v, 1)
        self.assertEqual(LE(self.d1, self.d0).v, 0)
        self.assertTrue(np.array_equal(LE(self.f0, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(LE(self.f1, self.f1).v, self.f1.v))
        self.assertTrue(np.array_equal(LE(self.f12, self.f12).v, np.array([0.25, 0.75] + [0.0] * (M-2))))
        self.assertTrue(np.array_equal(LE(self.f12, self.f23).v, self.f1.v))
        self.assertTrue(np.array_equal(LE(self.f23, self.f12).v, np.array([0.75, 0.25] + [0.0] * (M-2))))

    def test_EQ(self):
        self.assertEqual(EQ(self.d0, self.d0).v, 1)
        self.assertEqual(EQ(self.d0, self.d1).v, 0)
        self.assertTrue(np.array_equal(EQ(self.f0, self.f0).v, self.f1.v))
        self.assertTrue(np.array_equal(EQ(self.f1, self.f0).v, self.f0.v))
        self.assertTrue(np.array_equal(EQ(self.f12, self.f1).v, np.array([0.5, 0.5] + [0.0] * (M-2))))
        self.assertTrue(np.array_equal(EQ(self.f12, self.f23).v, np.array([0.75, 0.25] + [0.0] * (M-2))))

    def test_MIN(self):
        self.assertEqual(MIN(self.d0, self.d0).v, self.d0.v)
        self.assertEqual(MIN(self.d0, self.d1).v, self.d0.v)
        self.assertEqual(MIN(self.d1, self.d0).v, self.d0.v)
        self.assertTrue(np.array_equal(MIN(self.f0, self.f0).v, self.f0.v))
        self.assertTrue(np.array_equal(MIN(self.f1, self.f0).v, self.f0.v))
        self.assertTrue(np.array_equal(MIN(self.f0, self.f1).v, self.f0.v))
        self.assertTrue(np.array_equal(MIN(self.f1, self.f12).v, np.array([0.0, 1.0] + [0.0] * (M-2))))
        self.assertTrue(np.array_equal(MIN(self.f23, self.f12).v, np.array([0.0, 0.5, 0.5] + [0.0] * (M-3))))




