from tests.strategy import open_digraph_strategy, random_well_formed_open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_matrix_mx_test(unittest.TestCase):
    @given(random_well_formed_open_digraph_strategy(form='loop-free undirected'))
    def test_random_loop_free_undirected_open_digraph(self, graph):
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_children_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_child_multiplicity(node_id))

    @given(random_well_formed_open_digraph_strategy(form='undirected'))
    def test_random_undirected_open_digraph(self, graph):
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_children_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_child_multiplicity(node_id))

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
