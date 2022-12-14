from tests.strategy import random_well_formed_open_digraph_strategy
from modules.open_digraph import open_digraph
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_special_graph_mx_test(unittest.TestCase):
    @given(st.integers(max_value=20))
    def test_identity(self, n):
        if n >= 0:
            graph = open_digraph.identity(n)
            self.assertEqual(len(graph.get_id_node_map()), 2 * n)
            self.assertEqual(len(graph.get_input_ids()), n)
            self.assertEqual(len(graph.get_output_ids()), n)
            for inid in graph.get_input_ids():
                inode = graph.get_node_by_id(inid)
                self.assertIn(inode.get_children_ids()[0], graph.get_output_ids())
        else:
            self.assertRaises(ValueError, open_digraph.identity, n)
    
    @given(random_well_formed_open_digraph_strategy(form='loop-free undirected'))
    def test_random_loop_free_undirected_open_digraph(self, graph):
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_parent_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_parent_multiplicity(node_id))

    @given(random_well_formed_open_digraph_strategy(form='undirected'))
    def test_random_undirected_open_digraph(self, graph):
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_parent_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_parent_multiplicity(node_id))

    @given(random_well_formed_open_digraph_strategy(form='oriented'))
    def test_random_oriented_open_digraph(self, graph):
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertNotIn(node_id, child.get_children_ids())

    @given(random_well_formed_open_digraph_strategy(form='DAG'))
    def test_random_DAG_open_digraph(self, graph):
        self.assertFalse(graph.is_cyclic())
