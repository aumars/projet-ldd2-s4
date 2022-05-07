from modules.utils import *
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
    def setUp(self):
        self.r_bad = [1] * 3
        self.r0 = [0] * 8
        self.r1 = [1] * 8
        self.r = [0, 1, 1, 1, 1, 1, 1, 1]
        self.r230 = [1, 1, 1, 0, 0, 1, 1, 0]
        self.r245 = [1, 1, 1, 1, 0, 1, 0, 1]
        self.r475 = [1, 1, 1, 0, 1, 1, 0, 1]
        
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

    def test_code_gray_open_digraph(self):
        CG0 = gray_code(0)
        CG0_EXACT = [""]
        self.assertListEqual(CG0, CG0_EXACT)

        CG1 = gray_code(1)
        CG1_EXACT = ["0", "1"]
        self.assertListEqual(CG1, CG1_EXACT)

        CG7 = gray_code(3)
        CG7_EXACT = ["000", "001", "011", "010", "110", "111", "101", "100"]
        self.assertListEqual(CG7, CG7_EXACT)

    def test_K_map_open_digraph(self):
        self.assertRaises(ValueError, K_map, "1234")
        self.assertRaises(ValueError, K_map, "11100")
        self.assertListEqual(K_map(""), [])

        M1 = K_map("1110001000111111")
        T1_KARNAUGH = [[1, 1, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1], [0, 0, 1, 1]]
        self.assertListEqual(M1, T1_KARNAUGH)

    @unittest.skip("bit_string_to_formula utility function is not implemented.")
    def test_bit_string_to_formula_open_digraph(self):
        self.assertRaises(ValueError, K_map, "1234")
        self.assertEqual("(x0&x2)",  bit_string_to_formula("1100"))

        OP1 = "1110001000111111"
        F1 = bit_string_to_formula(OP1)
        F1_EXACT = "(x0&x2)|(x2&~x3)|(x0&x1)|(~x0&~x1&~x2)"
        self.assertEqual(F1, F1_EXACT)
