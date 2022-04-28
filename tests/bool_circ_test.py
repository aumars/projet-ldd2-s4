from modules.node import node
from modules.bool_circ import bool_circ
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class Bool_CircTest(unittest.TestCase):
    def setUp(self):
        self.B = bool_circ.empty()
        self.id3 = self.B.add_node('')
        self.id4 = self.B.add_node('&')
        self.id5 = self.B.add_node('|')
        self.id6 = self.B.add_node('~')
        self.id7 = self.B.add_node('|')

        self.B.add_edge(self.id3, self.id4)
        self.B.add_edge(self.id3, self.id5)
        self.B.add_edge(self.id4, self.id7)
        self.B.add_edge(self.id5, self.id6)
        self.B.add_edge(self.id6, self.id7)
        self.id0 = self.B.add_input_node(self.id4)
        self.id1 = self.B.add_input_node(self.id3)
        self.id2 = self.B.add_input_node(self.id5)
        self.B.get_node_by_id(self.id0).set_label('0')
        self.B.get_node_by_id(self.id1).set_label('1')
        self.B.get_node_by_id(self.id2).set_label('0')
        self.id8 = self.B.add_output_node(self.id7)

        self.C = self.B.copy()
        self.id_copy = self.C.add_node('')
        self.id_xor = self.C.add_node('^')
        self.C.remove_edge(self.id0, self.id4)
        self.C.add_edge(self.id0, self.id_copy)
        self.C.add_edge(self.id_copy, self.id_xor)
        self.C.add_edge(self.id_copy, self.id4)
        self.C.add_edge(self.id3, self.id_xor)
        self.C.add_edge(self.id_xor, self.id7)

        self.D = self.B.copy()
        self.id_extra0 = self.D.add_input_node(self.id5)

        self.LEGAL_LABELS = set(['0', '1', '&', '|', '~', "~", ''])

    def test_well_formed_bool_circ(self):
        self.assertTrue(self.B.is_well_formed())
        self.assertTrue(self.C.is_well_formed())

    def test_well_formed_primitives(self):
        self.assertTrue(self.D.is_well_formed())

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

    def test_adder(self):
        self.assertTrue(bool_circ.adder(0).is_well_formed())
        self.assertTrue(bool_circ.adder(1).is_well_formed())
        self.assertTrue(bool_circ.adder(4).is_well_formed())

    def test_half_adder(self):
        self.assertTrue(bool_circ.half_adder(0).is_well_formed())
        self.assertTrue(bool_circ.half_adder(1).is_well_formed())
        self.assertTrue(bool_circ.half_adder(4).is_well_formed())

    def test_register(self):
        g = bool_circ.register(8, 11)

        n0 = 0
        n1 = 0
        n_autre = 0
        for n in g.get_input_ids():
            node = g.get_node_by_id(n)
            if node.get_label() == '0':
                n0 += 1
            elif node.get_label() == '1':
                n1 += 1
            else:
                n_autre += 1

        self.assertEqual(n0, 5)
        self.assertEqual(n1, 3)
        self.assertEqual(n_autre, 0)

    def test_trans_copy_valid(self):
        self.B.trans_copy([self.id1])
        self.assertNotIn(self.id1, self.B.get_node_ids())
        self.assertNotIn(self.id3, self.B.get_node_ids())
        n4 = self.B.get_node_by_id(self.id4)
        n5 = self.B.get_node_by_id(self.id5)
        self.assertEqual(2, n4.indegree())
        self.assertEqual(2, n5.indegree())
        self.assertCountEqual({'0': 1, '1': 1}, [self.B.get_node_by_id(parent).get_label() for parent in n4.get_parent_ids()])
        self.assertCountEqual({'0': 1, '1': 1}, [self.B.get_node_by_id(parent).get_label() for parent in n5.get_parent_ids()])
        self.assertTrue(self.B.is_well_formed())

    def test_trans_copy_invalid(self):
        self.B.trans_copy([self.id0])
        self.assertIn(self.id0, self.B.get_node_ids())
        self.assertIn(self.id4, self.B.get_node_ids())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_not_valid(self):
        self.B.get_node_by_id(self.id3).set_label('~')
        self.B.trans_not([self.id1])
        self.assertNotIn(self.id1, self.B.get_node_ids())
        self.assertIn(self.id3, self.B.get_node_ids())
        self.assertEqual('0', self.B.get_node_by_id(self.id3).get_label())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_and_valid0(self):
        self.B.trans_and([self.id0])
        self.assertNotIn(self.id0, self.B.get_node_ids())
        n3 = self.B.get_node_by_id(self.id3)
        n4 = self.B.get_node_by_id(self.id4)
        self.assertEqual('0', n4.get_label())
        self.assertEqual(0, n4.indegree())
        self.assertEqual(2, n3.outdegree())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_and_valid1(self):
        self.B.get_node_by_id(self.id0).set_label('1')
        self.B.trans_and([self.id0])
        self.assertNotIn(self.id0, self.B.get_node_ids())
        n3 = self.B.get_node_by_id(self.id3)
        n4 = self.B.get_node_by_id(self.id4)
        self.assertEqual('&', n4.get_label())
        self.assertEqual(1, n4.indegree())
        self.assertEqual(2, n3.outdegree())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_xor_valid0(self):
        self.B.trans_xor([self.id0])
        self.assertTrue(self.B.is_well_formed())

    def test_trans_xor_valid1(self):
        g = bool_circ.empty()
        id0 = g.add_node('0')
        id1 = g.add_node('1')
        id2 = g.add_node('~')
        g.add_edge(id0, id2)
        g.add_edge(id1, id2)
        g.trans_xor([id0])
        self.assertNotIn(id0, g.get_node_ids())
        self.assertIn(id1, g.get_node_ids())
        self.assertIn(id2, g.get_node_ids())

        g.trans_xor([id1])
        self.assertNotIn(id1, g.get_node_ids())
        self.assertIn(id2, g.get_node_ids())
        self.assertEqual(len(g.get_node_by_id(id2).get_children_ids()), 1)

    def test_trans_neutre(self):
        self.B.trans_neutral([self.id0])
        self.assertTrue(self.B.is_well_formed())

    def test_transform_all(self):
        A0 = bool_circ.adder(0)
        A0.get_node_by_id(A0.get_input_ids()[0]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[1]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        A0.transform_all()
        self.assertTrue(A0.is_well_formed())

    def test_transform_full(self):
        A0 = bool_circ.adder(0)
        A0.get_node_by_id(A0.get_input_ids()[0]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[1]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        while len(A0.get_output_ids()) != len(A0.get_node_ids()):
            A0.transform_all()
            self.assertTrue(A0.is_well_formed())

    def test_evaluate(self):
        A0 = bool_circ.adder(0)
        A0.get_node_by_id(A0.get_input_ids()[0]).set_label('0')
        A0.get_node_by_id(A0.get_input_ids()[1]).set_label('0')
        A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        self.assertEqual("00", A0.evaluate())

        A0.get_node_by_id(A0.get_input_ids()[0]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[1]).set_label('0')
        A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        self.assertEqual("01", A0.evaluate())

        #A0.get_node_by_id(A0.get_input_ids()[0]).set_label('0')
        #A0.get_node_by_id(A0.get_input_ids()[1]).set_label('1')
        #A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        #self.assertEqual("01", A0.evaluate())

        A0.get_node_by_id(A0.get_input_ids()[0]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[1]).set_label('1')
        A0.get_node_by_id(A0.get_input_ids()[2]).set_label('0')
        self.assertEqual("11", A0.evaluate())
        #A8 = bool_circ.adder(8)
        #A8.evaluate()
        #self.assertTrue(A8.is_well_formed())

    @unittest.skip
    def test_add_bool_circ(self):
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
    def test_half_add_bool_circ(self):
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
