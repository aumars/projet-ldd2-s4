from tests.strategy import open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_connected_components_mx_test(unittest.TestCase):
    @unittest.skip
    @given(open_digraph_strategy())
    def test_connected_components_open_digraph(self, graph):
        n, d = graph.connected_components()
        ids = graph.get_node_ids()
        self.assertGreaterEqual(n, 0)
        for k, v in d.items():
            self.assertIn(k, ids)
            self.assertLessEqual(v, n)

    @unittest.skip
    @given(open_digraph_strategy())
    def test_get_connected_components_open_digraph(self, graph):
        l = graph.get_connected_components()
        n, _ = graph.connected_components()
        inputs1 = len(graph.get_input_ids())
        outputs1 = len(graph.get_output_ids())
        nodes1 = len(graph.get_id_node_map())
        inputs2 = sum([len(g.get_input_ids()) for g in l])
        outputs2 = sum([len(g.get_output_ids()) for g in l])
        nodes2 = sum([len(g.get_id_node_map()) for g in l])
        self.assertEqual(len(l), n)
        self.assertEqual(nodes1, nodes2)
        self.assertEqual(inputs1, inputs2)
        self.assertEqual(outputs1, outputs2)
