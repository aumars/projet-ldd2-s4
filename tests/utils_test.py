from random import randrange
from modules.utils import *
import unittest
import numpy as np
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)


class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_random_int_list(self):
        n, bound = randrange(100), randrange(100)
        arr = np.asarray(random_int_list(n, bound))
        self.assertEqual(n, arr.shape[0])
        self.assertTrue((arr <= bound).all())

        arr_empty = np.asarray(random_int_list(0, 10))
        self.assertEqual(0, arr_empty.shape[0])

    def test_random_int_matrix(self):
        n, bound = randrange(1, 100), randrange(100)

        m_no_diag_null = random_int_matrix(n, bound, null_diag=False)
        m_diag_null = random_int_matrix(n, bound, null_diag=True)
        m_no_diag_null = np.asarray(m_no_diag_null)
        m_diag_null = np.asarray(m_diag_null)

        self.assertEqual((n, n, ), m_no_diag_null.shape)
        self.assertEqual((n, n, ), m_diag_null.shape)

        self.assertTrue(
            np.asarray([m_no_diag_null[i] <= bound for i in range(n)]).all())

        self.assertTrue(
            np.asarray([m_diag_null[i] <= bound for i in range(n)]).all())

        self.assertTrue((m_diag_null.diagonal() == 0).all())

    def test_random_symetric_int_matrix(self):
        n, bound = randrange(1, 100), randrange(100)

        m_no_diag_null = random_symetric_int_matrix(n, bound, null_diag=False)
        m_diag_null = random_symetric_int_matrix(n, bound, null_diag=True)
        m_no_diag_null = np.asarray(m_no_diag_null)
        m_diag_null = np.asarray(m_diag_null)

        self.assertEqual((n, n, ), m_no_diag_null.shape)
        self.assertEqual((n, n, ), m_diag_null.shape)

        self.assertTrue(
            np.asarray([m_no_diag_null[i] <= bound for i in range(n)]).all())

        self.assertTrue(
            np.asarray([m_diag_null[i] <= bound for i in range(n)]).all())

        self.assertTrue((m_no_diag_null == m_no_diag_null.T).all())
        self.assertTrue((m_diag_null == m_diag_null.T).all())

        self.assertTrue((m_diag_null.diagonal() == 0).all())

    def test_random_oriented_int_matrix(self):
        n, bound = randrange(100), randrange(100)

        m_no_diag_null = random_oriented_int_matrix(n, bound, null_diag=False)
        m_diag_null = random_oriented_int_matrix(n, bound, null_diag=True)
        m_no_diag_null = np.asarray(m_no_diag_null)
        m_diag_null = np.asarray(m_diag_null)

        self.assertEqual((n, n, ), m_no_diag_null.shape)
        self.assertEqual((n, n, ), m_diag_null.shape)

        self.assertTrue(
            np.asarray([m_no_diag_null[i] <= bound for i in range(n)]).all())

        self.assertTrue(
            np.asarray([m_diag_null[i] <= bound for i in range(n)]).all())

        m_diag_is_oriented = [m_diag_null[j][i] == 0 if m_diag_null[i][j] != 0
                              else True
                              for i in range(n) for j in range(n)]

        m_no_diag_is_oriented = [m_no_diag_null[j][i] == 0 if m_no_diag_null[i][j] != 0
                                 else True
                                 for i in range(n) for j in range(n)]


        self.assertTrue(np.asarray(m_diag_is_oriented).all())
        self.assertTrue(np.asarray(m_no_diag_is_oriented).all())

        self.assertTrue((m_diag_null.diagonal() == 0).all())

    def test_random_triangular_int_matrix(self):
        n, bound = randrange(1, 100), randrange(100)
        m_trian_sup = np.triu_indices(n, 1)

        m_no_diag_null = random_triangular_int_matrix(
            n, bound, null_diag=False)
        m_diag_null = random_triangular_int_matrix(n, bound, null_diag=True)
        m_no_diag_null = np.asarray(m_no_diag_null)
        m_diag_null = np.asarray(m_diag_null)

        self.assertTrue((m_no_diag_null[m_trian_sup] == 0).all())
        self.assertTrue((m_diag_null[m_trian_sup] == 0).all())

        self.assertTrue((m_diag_null.diagonal() == 0).all())
