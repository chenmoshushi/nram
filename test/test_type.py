from model.interpreter.datatype import DataType, Discrete, Fuzzy

import unittest
import numpy as np

class TestTypeConstruction(unittest.TestCase):

    def test_typeEqualityOnDistruct(self):
        self.assertEqual(Discrete(42).v, 42)
        self.assertTrue(np.array_equal(Fuzzy(np.zeros(42)).v, np.zeros(42)))
    
    def test_typeMismatch(self):
        with self.assertRaises(TypeError):
            Discrete(np.zeros(42))
        with self.assertRaises(TypeError):
            Fuzzy(42)



