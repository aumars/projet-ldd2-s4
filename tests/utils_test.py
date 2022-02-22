from modules.utils import (random_int_list,
                           random_int_matrix,
                           random_symetric_int_matrix,
                           random_oriented_int_matrix,
                           random_triangular_int_matrix)
import unittest
import numpy as np
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)

capped_n = st.integers(max_value=20)
capped_bound = st.integers(max_value=10)


class UtilsTest(unittest.TestCase):
    @given(capped_n, capped_bound)
    def test_random_int_list_utils(self, n, bound):
        if n < 0 or (n > 0 and bound < 0):
            self.assertRaises(ValueError, random_int_list, n, bound)
        else:
            arr = np.asarray(random_int_list(n, bound))
            self.assertEqual((n,), arr.shape)
            self.assertTrue(np.all(arr <= bound))

    @given(capped_n, capped_bound, st.booleans())
    def test_random_int_matrix_utils(self, n, bound, null_diag):
        if n < 0 or (n > 0 and bound < 0):
            self.assertRaises(ValueError, random_int_matrix, n, bound, null_diag)
        else:
            A = random_int_matrix(n, bound, null_diag)
            A = np.asarray(A)
            self.assertTrue(np.all(A <= np.full(A.shape, bound)))
            if n == 0:
                self.assertEqual((0,), A.shape)
            else:
                self.assertEqual((n, n,), A.shape)
                if null_diag:
                    self.assertTrue(np.all(A.diagonal() == 0))

    @given(capped_n, capped_bound, st.booleans())
    def test_random_symetric_int_matrix_utils(self, n, bound, null_diag):
        if n < 0 or (n > 0 and bound < 0):
            self.assertRaises(ValueError, random_symetric_int_matrix, n, bound, null_diag)
        else:
            A = random_symetric_int_matrix(n, bound, null_diag)
            A = np.asarray(A)
            self.assertTrue(np.all(A <= np.full(A.shape, bound)))
            self.assertTrue(np.all(A == A.T))
            if n == 0:
                self.assertEqual((0,), A.shape)
            else:
                self.assertEqual((n, n,), A.shape)
                if null_diag:
                    self.assertTrue(np.all(A.diagonal() == 0))

    @given(capped_n, capped_bound, st.booleans())
    def test_random_oriented_int_matrix_utils(self, n, bound, null_diag):
        if n < 0 or (n > 0 and bound < 0):
            self.assertRaises(ValueError, random_oriented_int_matrix, n, bound, null_diag)
        else:
            A = random_oriented_int_matrix(n, bound, null_diag)
            A = np.asarray(A)
            self.assertTrue(np.all(A <= np.full(A.shape, bound)))
            if n == 0:
                self.assertEqual((0,), A.shape)
            else:
                self.assertEqual((n, n,), A.shape)
                nonzero = np.nonzero(A)
                if null_diag:
                    self.assertTrue(np.all(A.diagonal() == 0))
                else:
                    np.fill_diagonal(A, 0)
                self.assertTrue(np.all(A.T[nonzero] == 0))

    @given(capped_n, capped_bound, st.booleans())
    def test_random_triangular_int_matrix_utils(self, n, bound, null_diag):
        if n < 0 or (n > 0 and bound < 0):
            self.assertRaises(ValueError, random_triangular_int_matrix, n, bound, null_diag)
        else:
            A = random_triangular_int_matrix(n, bound, null_diag)
            A = np.asarray(A)
            m_trian_sup = np.triu_indices(n, 1)
            if n == 0:
                self.assertEqual((0,), A.shape)
            else:
                self.assertEqual((n, n,), A.shape)
                self.assertTrue(np.all(A[m_trian_sup] == 0))
                if null_diag:
                    self.assertTrue(np.all(A.diagonal() == 0))
