from model.interpreter.datatype import DataType, Discrete, Fuzzy
from model.interpreter.module import Zero, One, Add

import unittest
import numpy as np

class TestModuleImplementation(unittest.TestCase):

    def test_type_construction(self):
        self.assertEqual(Discrete(42).v, 42)
        self.assertTrue(np.array_equal(Fuzzy(np.zeros(42)).v, np.zeros(42)))
        with self.assertRaises(TypeError):
            Discrete(np.zeros(42))
        with self.assertRaises(TypeError):
            Fuzzy(42)



