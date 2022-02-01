from modules.utils import utils
from modules.node import node
from modules.open_digraph import open_digraph
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)


class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.id = list(range(5))
        self.n0 = node(self.id[0], "v0", {3: 1}, {1: 1, 2: 1})
        self.n1 = node(self.id[1], "v1", {0: 1}, {3: 1, 4: 2})
        self.n2 = node(self.id[2], "v2", {0: 1}, {3: 2})
        self.n3 = node(self.id[3], "v3", {1: 1, 2: 2}, {0: 1, 4: 1})
        self.n4 = node(self.id[4], "v4", {}, {1: 2, 3: 1})

        self.g = open_digraph(
            [], [], [self.n0, self.n1, self.n2, self.n3, self.n4])

        self.Ag = [[0, 1, 1, 0, 0],
                   [0, 0, 0, 1, 2],
                   [0, 0, 0, 2, 0],
                   [1, 0, 0, 0, 1],
                   [0]*5]

    def test_random_int_list(self):
        self.assertRaises(ValueError, utils.test_random_int_list, -2, 10, True)
        l1 = utils.random_int_list(5, 10)
        self.assertEqual(5, len(l1))

    def test_random_int_matrix(self):
        self.assertRaises(ValueError, utils.random_int_matrix, -2, 10, True)

        n = 3
        m = utils.random_int_matrix(n, 10, null_diag=True)
        self.assertEqual(n, len(m))
        self.assertEqual(n, len(m[0]))
        self.assertListEqual([0] * n, [m[i][i] for i in range(n)])

    def test_random_symetric_int_matrix(self):
        self.assertRaises(
            ValueError, utils.random_symetric_int_matrix, -2, 10, True)

        n = 10
        m_no_diag = utils.random_symetric_int_matrix(n, 10, null_diag=False)
        self.assertListEqual([m_no_diag[i][j] for i in range(n) for j in range(n)],
                             [m_no_diag[j][i] for i in range(n) for j in range(n)])

        m_diag = utils.random_symetric_int_matrix(n, 10, null_diag=True)
        self.assertListEqual([0] * n, [m_diag[i][i] for i in range(n)])

    def test_random_oriented_int_matrix(self):
        n1 = 5
        m1 = utils.random_oriented_int_matrix(n1, 10, null_diag=True)
        self.assertListEqual([0] * n1, [m1[i][i] for i in range(n1)])

        n2 = 5
        m2 = utils.random_oriented_int_matrix(n2, 10, null_diag=False)

        self.assertListEqual([0]*n2,
                             [m2[j][i] for i in range(n2) for j in range(i, n2)])

    def test_random_triangular_int_matrix(self):
        n = 6
        m = utils.random_triangular_int_matrix(n, 5, True)
        self.assertListEqual([0] * n, [m[i][i] for i in range(n)])
        self.assertListEqual([0]*n,
                             [m[i][j] for i in range(n) for j in range(i, n)])

    def test_graph_from_adjacency_matrix(self):
        g = utils.graph_from_adjacency_matrix(self.Ag)
        print(g)
        print(self.g)

    def test_random(self):
        n = 7

        m_dag = utils.random(n, 3, inputs=2, outputs=1, form="DAG")
        m_oriented = utils.random(n, 3, inputs=2, outputs=1, form="oriented")
        m_loop_free = utils.random(n, 3, inputs=2, outputs=1, form="loop-free")
        m_undirect = utils.random(n, 3, inputs=2, outputs=1, form="undirect")
        m_loop_free_undirect = self.random(
            n, 3, inputs=2, outputs=1, form="loop-free undirect")

        self.assertListEqual([0]*n,
                             [m_dag[i][j] for i in range(n) for j in range(i, n)])

        for i in range(n):
            for j in range(n):
                if m_oriented[i][j] != 0:
                    self.assertEqual(0, m_oriented[i][j])

        self.assertListEqual([0]*n, [m_loop_free[i][i] for i in range(n)])

        self.assertListEqual([0]*n, [m_undirect[i][i] for i in range(n)])

        for i in range(n):
            for j in range(n):
                if m_loop_free_undirect[i][j] != 0:
                    self.assertEqual(0, m_loop_free_undirect[i][j])
        
        self.assertListEqual([0]*n, [m_loop_free_undirect[i][i] for i in range(n)])

    def test_node_dict(self):
        S = set(self.id) & set(utils.node_dict(self.g).values())
        self.assertEqual(S, {})

