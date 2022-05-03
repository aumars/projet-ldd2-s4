from modules.node import node
from modules.bool_circ import bool_circ
import unittest
import sys
import os
from hypothesis import given, strategies as st
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
        self.C.get_node_by_id(self.id4).set_label('^')

        self.D = self.B.copy()
        self.id_extra0 = self.D.add_input_node(self.id5)
        self.D.get_node_by_id(self.id_extra0).set_label('0')

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

    def test_adder0(self):
        A0 = bool_circ.adder(0)
        self.assertEqual(3, len(A0.get_input_ids()))
        self.assertEqual(2, len(A0.get_output_ids()))
        self.assertTrue(A0.is_well_formed())

    def test_adder1(self):
        A1 = bool_circ.adder(1)
        self.assertEqual(5, len(A1.get_input_ids()))
        self.assertEqual(3, len(A1.get_output_ids()))
        self.assertTrue(A1.is_well_formed())

    def test_adder2(self):
        A2 = bool_circ.adder(2)
        self.assertEqual(9, len(A2.get_input_ids()))
        self.assertEqual(5, len(A2.get_output_ids()))
        self.assertTrue(A2.is_well_formed())

    def test_half_adder0(self):
        HA0 = bool_circ.half_adder(0)
        self.assertEqual(2, len(HA0.get_input_ids()))
        self.assertEqual(2, len(HA0.get_output_ids()))
        self.assertTrue(HA0.is_well_formed())

    def test_half_adder1(self):
        HA1 = bool_circ.half_adder(1)
        self.assertEqual(4, len(HA1.get_input_ids()))
        self.assertEqual(3, len(HA1.get_output_ids()))
        self.assertTrue(HA1.is_well_formed())

    def test_half_adder2(self):
        HA2 = bool_circ.half_adder(2)
        self.assertEqual(8, len(HA2.get_input_ids()))
        self.assertEqual(5, len(HA2.get_output_ids()))
        self.assertTrue(HA2.is_well_formed())

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

    def test_trans_not_valid0(self):
        self.B.get_node_by_id(self.id1).set_label('0')
        self.B.get_node_by_id(self.id3).set_label('~')
        self.B.trans_not([self.id1])
        self.assertNotIn(self.id1, self.B.get_node_ids())
        self.assertIn(self.id3, self.B.get_node_ids())
        self.assertEqual('1', self.B.get_node_by_id(self.id3).get_label())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_not_valid1(self):
        self.B.get_node_by_id(self.id3).set_label('~')
        self.B.trans_not([self.id1])
        self.assertNotIn(self.id1, self.B.get_node_ids())
        self.assertIn(self.id3, self.B.get_node_ids())
        self.assertEqual('0', self.B.get_node_by_id(self.id3).get_label())
        self.assertTrue(self.B.is_well_formed())

    def test_trans_not_invalid(self):
        self.B.trans_not([self.id0])
        self.assertIn(self.id0, self.B.get_node_ids())
        self.assertIn(self.id4, self.B.get_node_ids())
        self.assertEqual('0', self.B.get_node_by_id(self.id0).get_label())
        self.assertEqual('&', self.B.get_node_by_id(self.id4).get_label())
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
        self.C.trans_xor([self.id0])
        self.assertNotIn(self.id0, self.C.get_node_ids())
        self.assertTrue(self.C.is_well_formed())

    def test_trans_xor_valid1(self):
        node4 = self.C.get_node_by_id(self.id4)
        self.C.get_node_by_id(self.id0).set_label('1')
        self.C.trans_xor([self.id0])
        self.assertTrue(self.C.is_well_formed())
        self.assertNotIn(self.id0, self.C.get_node_ids())
        self.assertEqual(1, node4.indegree())
        self.assertEqual(1, node4.outdegree())
        self.assertNotIn(7, node4.get_children_ids())
        node4_child = self.C.get_node_by_id(node4.get_children_ids()[0])
        self.assertEqual('~',  node4_child.get_label())
        self.assertEqual(1, node4_child.outdegree())
        self.assertIn(self.id7, node4_child.get_children_ids())

    def test_trans_neutre(self):
        self.B.trans_neutral([self.id0])
        self.assertTrue(self.B.is_well_formed())

    def test_transform_all(self):
        A0 = bool_circ.half_adder(0)
        A0.set_input_bits("11")
        A0.transform_all()
        self.assertTrue(A0.is_well_formed())

    def test_transform_full(self):
        A0 = bool_circ.half_adder(0)
        A0.set_input_bits("11")
        outputs = len(A0.get_output_ids())
        while len(A0.get_output_ids()) != len(A0.get_node_ids()):
            A0.transform_all()
            self.assertTrue(A0.is_well_formed())
            self.assertEqual(outputs, len(A0.get_output_ids()))

    def test_evaluate_adder(self):
        A0 = bool_circ.adder(0)

        A0.set_input_bits("000")
        self.assertEqual("00", A0.evaluate())

        A0.set_input_bits("001")
        self.assertEqual("01", A0.evaluate())

        A0.set_input_bits("010")
        self.assertEqual("01", A0.evaluate())

        A0.set_input_bits("011")
        self.assertEqual("10", A0.evaluate())

        A0.set_input_bits("100")
        self.assertEqual("01", A0.evaluate())

        A0.set_input_bits("101")
        self.assertEqual("10", A0.evaluate())

        A0.set_input_bits("110")
        self.assertEqual("10", A0.evaluate())

        A0.set_input_bits("111")
        self.assertEqual("11", A0.evaluate())

    def test_evaluate_half_adder(self):
        A0 = bool_circ.half_adder(0)

        A0.set_input_bits("00")
        self.assertEqual("00", A0.evaluate())

        A0.set_input_bits("01")
        self.assertEqual("01", A0.evaluate())

        A0.set_input_bits("10")
        self.assertEqual("01", A0.evaluate())

        A0.set_input_bits("11")
        self.assertEqual("10", A0.evaluate())

    @unittest.skip
    def test_hamming_bool_circ(self):
        ENC = bool_circ.encoder()
        DEC = bool_circ.decoder()
        replace_bit = lambda n, enc_eval: "1" if enc_eval[n] == "0" else "0" 

        b0 = "0000"
        ENC.set_input_bits(b0)
        DEC.set_input_bits(ENC.evaluate())
        self.assertEqual(b0, DEC.evaluate())

        b1 = "1111"
        ENC.set_input_bits(b1)
        DEC.set_input_bits(ENC.evaluate())
        self.assertEqual(b1, DEC.evaluate())

        b1 = "1001"
        ENC.set_input_bits(b1)
        DEC.set_input_bits(ENC.evaluate())
        self.assertEqual(b1, DEC.evaluate())

        b2 = "1001"
        ENC.set_input_bits(b2)
        enc_eval = ENC.evaluate()
        DEC.set_input_bits(enc_eval[:-1]+replace_bit(-1, enc_eval))
        self.assertEqual(b2, DEC.evaluate())

        b3 = "1010"
        ENC.set_input_bits(b2)
        enc_eval = ENC.evaluate()
        DEC.set_input_bits(enc_eval[:-2]+replace_bit(-2, enc_eval)+replace_bit(-1, enc_eval))
        self.assertNotEqual(b3, DEC.evaluate())

    @given(st.integers(min_value=0, max_value=10),
           st.integers(min_value=0, max_value=10))
    def test_add(self, a, b):
        c = a + b
        res, overflow, bits = bool_circ.add(a, b)
        if overflow:
            self.assertEqual(res, c % bits)
        else:
            self.assertEqual(c, res)
