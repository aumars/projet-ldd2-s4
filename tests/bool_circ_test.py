from modules.node import node
from modules.bool_circ import bool_circ
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class Bool_CircTest(unittest.TestCase):
    def setUp(self):
        nodes = []
        nodes.append(node(0, 'x0', {}, {4: 1}))
        nodes.append(node(1, 'x1', {}, {3: 1}))
        nodes.append(node(2, 'x2', {}, {5: 1}))
        nodes.append(node(3, '', {1: 1}, {4: 1, 5: 1}))
        nodes.append(node(4, '&', {0: 1, 3: 1}, {7: 1}))
        nodes.append(node(5, '|', {2: 1, 3: 1}, {6: 1}))
        nodes.append(node(6, '~', {5: 1}, {7: 1}))
        nodes.append(node(7, '|', {4: 1}, {8: 1}))
        nodes.append(node(8, 'r0', {7: 1}, {}))
        self.B = bool_circ([0, 1, 2], [8], nodes)

        self.LEGAL_LABELS = set(["&", "|", "~", ""])

    def test_well_formed_bool_circ(self):
        self.assertTrue(self.B.is_well_formed())

    def test_illegal_labels_bool_circ(self):
        nodes = []
        nodes.append(node(0, 'x0', {}, {4: 1}))
        nodes.append(node(1, 'x1', {}, {3: 1}))
        nodes.append(node(2, 'x2', {}, {5: 1}))
        nodes.append(node(3, 'COPIE', {1: 1}, {4: 1, 5: 1}))
        nodes.append(node(4, 'AND', {0: 1, 3: 1}, {7: 1}))
        nodes.append(node(5, 'OR', {2: 1, 3: 1}, {6: 1}))
        nodes.append(node(6, 'NOT', {5: 1}, {7: 1}))
        nodes.append(node(7, 'OR', {4: 1}, {8: 1}))
        nodes.append(node(8, 'r0', {7: 1}, {}))
        B2 = bool_circ([0, 1, 2], [8], nodes)
        self.assertFalse(B2.is_well_formed())

    def test_cyclic_bool_circ(self):
        nodes = []
        nodes.append(node(0, 'x0', {}, {4: 1}))
        nodes.append(node(1, 'x1', {}, {3: 1}))
        nodes.append(node(2, 'x2', {}, {5: 1}))
        nodes.append(node(3, '', {1: 1}, {4: 1, 5: 1}))
        nodes.append(node(4, '&', {0: 1, 3: 1}, {7: 1}))
        nodes.append(node(5, '|', {2: 1, 3: 1, 5: 1}, {6: 1}))
        nodes.append(node(6, '~', {5: 1}, {7: 1}))
        nodes.append(node(7, '|', {4: 1, 7: 1}, {5: 1, 8: 1}))
        nodes.append(node(8, 'r0', {7: 1}, {}))
        self.assertRaises(ValueError, bool_circ, [0, 1, 2], [8], nodes)
        # B2 = bool_circ([0, 1, 2], [8], nodes)
        # self.assertFalse(B2.is_well_formed())

    def test_illegal_degree_bool_circ(self):
        nodes = []
        nodes.append(node(0, 'x0', {}, {4: 1}))
        nodes.append(node(1, 'x1', {}, {3: 1}))
        nodes.append(node(2, 'x2', {}, {5: 1}))
        nodes.append(node(3, '', {1: 1}, {4: 1, 5: 1}))
        nodes.append(node(4, '&', {0: 1, 3: 1}, {6: 1, 7: 1}))
        nodes.append(node(5, '|', {2: 1, 3: 1}, {6: 1}))
        nodes.append(node(6, '~', {4: 1, 5: 1}, {7: 1}))
        nodes.append(node(7, '|', {4: 1}, {8: 1}))
        nodes.append(node(8, 'r0', {7: 1}, {}))
        B2 = bool_circ([0, 1, 2], [8], nodes)
        self.assertFalse(B2.is_well_formed())

    def test_from_formula_empty_bool_circ(self):
        B_EMPTY = bool_circ.from_formula("")
        self.assertFalse(B_EMPTY.is_well_formed())

    def test_from_formula_copy_bool_circ(self):
        B_COPY = bool_circ.from_formula("(x0)")
        self.assertEqual(len(B_COPY.get_node_ids()), 4)
        self.assertTrue(B_COPY.is_well_formed())

    def test_from_formula_example1_bool_circ(self):
        B0 = bool_circ.from_formula("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
        self.assertTrue(B0.is_well_formed())
        self.assertEqual(len(B0.get_node_ids()), 12)
        labels = set([n.get_label() for n in B0.get_nodes()])
        self.assertEqual(labels - self.LEGAL_LABELS, set())

    def test_from_formula_example2_bool_circ(self):
        B1 = bool_circ.from_formula("((x0)&((x1)&(x2)))|((x1)&(~(x2)))", "((x0)&(~(x1)))|(x2)")
        self.assertTrue(B1.is_well_formed())
        self.assertEqual(len(B1.get_node_ids()), 16)
        labels = set([n.get_label() for n in B1.get_nodes()])
        self.assertEqual(labels - self.LEGAL_LABELS, set())

    def test_from_binary_bool_circ(self):
        self.assertRaises(ValueError, bool_circ.from_binary, "10101")
        self.assertRaises(ValueError, bool_circ.from_binary, "1234")

        B1 = bool_circ.from_binary("1")
        self.assertTrue(B1.is_well_formed())

        B2 = bool_circ.from_binary("1110001000111111")
        self.assertTrue(B2.is_well_formed())
        self.assertEqual(4, len(B2.get_input_ids()))
        self.assertEqual(1, len(B2.get_output_ids()))

    def test_random_bool_circ(self):       
        B1 = bool_circ.random(1)
        self.assertTrue(B1.is_well_formed())
        self.assertEqual(1, len(B1.get_input_ids()))
        self.assertEqual(1, len(B1.get_output_ids()))

        B10 = bool_circ.random(10)
        self.assertTrue(B10.is_well_formed())
        self.assertEqual(10, len(B10.get_input_ids()))
        self.assertEqual(10, len(B10.get_output_ids()))

    @unittest.skip
    def test_adder_bool_circ(self):
        r_bad = [0, 1, 0, 1, 0]
        r0 = [0] * 8
        r1 = [1] * 8

        self.assertRaises(ValueError, bool_circ.adder, r_bad, r1)
        self.assertRaises(ValueError, bool_circ.adder, r1, r_bad)

        sum0, carry = bool_circ.adder(r0, r0)
        self.assertListEqual(sum0, r0)
        self.assertListEqual(carry, 0)

        sum1, carry = bool_circ.adder(r0, r1)
        self.assertListEqual(sum1, r1)
        self.assertListEqual(carry, 1)

        sum1, carry = bool_circ.adder(r0, r1)
        self.assertListEqual(sum1, r1)
        self.assertListEqual(carry, 1)

    @unittest.skip
    def test_half_adder_bool_circ(self):
        r_bad = [0, 1, 0, 1, 0]
        r0 = [0] * 8
        r1 = [1] * 8

        self.assertRaises(ValueError, bool_circ.half_adder, r_bad, r1)
        self.assertRaises(ValueError, bool_circ.half_adder, r1, r_bad)

        sum0, carry = bool_circ.half_adder(r0, r0)
        self.assertListEqual(sum0, r0)
        self.assertListEqual(carry, 0)

        sum1, carry = bool_circ.half_adder(r0, r1)
        self.assertListEqual(sum1, r1)
        self.assertListEqual(carry, 1)

        sum1, carry = bool_circ.half_adder(r0, r1)
        self.assertListEqual(sum1, r1)
        self.assertListEqual(carry, 1)
