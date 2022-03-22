from modules.node import node
from modules.open_digraph import open_digraph
from tests.strategy import open_digraph_strategy, random_well_formed_open_digraph_strategy
import numpy as np
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class Open_DigraphTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})

        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})

        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})

        self.G = open_digraph([3, 4], [5, 6], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])

        self.n0_2 = node(0, "v0", {3: 1}, {1: 1, 2: 1})
        self.n1_2 = node(1, "v1", {0: 1}, {3: 1, 4: 2})
        self.n2_2 = node(2, "v2", {0: 1}, {3: 2})
        self.n3_2 = node(3, "v3", {1: 1, 2: 2}, {0: 1, 4: 1})
        self.n4_2 = node(4, "v4", {}, {1: 2, 3: 1})

        self.G2 = open_digraph([], [], [self.n0_2, self.n1_2, self.n2_2, self.n3_2, self.n4_2])

    @given(open_digraph_strategy())
    def test_new_id_open_digraph(self, graph):
        """Test new_id method."""
        self.assertNotIn(graph.new_id(), graph.get_node_ids())

    @given(open_digraph_strategy())
    def test_min_id_open_digraph(self, graph):
        if len(graph.get_id_node_map()) > 0:
            self.assertEqual(graph.min_id(), min(graph.get_node_ids()))
        else:
            self.assertEqual(graph.min_id(), 0)

    @given(open_digraph_strategy())
    def test_max_id_open_digraph(self, graph):
        if len(graph.get_id_node_map()) > 0:
            self.assertEqual(graph.max_id(), max(graph.get_node_ids()))
        else:
            self.assertEqual(graph.max_id(), 0)

    @given(open_digraph_strategy())
    def test_copy_open_digraph(self, graph):
        """Test the copy method of open_digraph class."""
        self.assertIsNot(graph.copy(), graph)

    @given(open_digraph_strategy())
    def test_node_dict_open_digraph(self, graph):
        uniq_dict = open_digraph.node_dict(graph)
        vals = uniq_dict.values()
        ids = graph.get_node_ids()
        self.assertCountEqual(ids, uniq_dict.keys())
        self.assertEqual(len(set(vals)), len(vals))

    def test_is_well_formed_valid_graph_open_digraph(self):
        """Test is_well_formed method with a valid graph."""
        self.assertTrue(self.G.is_well_formed())

    def test_is_well_formed_invalid_graph_open_digraph(self):
        """Test is_well_formed method with an invalid graph."""
        G_not_well_formed = open_digraph([0, 4], [1, 2], [self.n0, self.n1])
        self.assertFalse(G_not_well_formed.is_well_formed())

    def test_is_well_formed_removing_edges_open_digraph(self):
        self.G.remove_edge(0, 2)

    def test_is_well_formed_adding_internal_nodes_open_digraph(self):
        """Test is_well_formed method with adding internal nodes to a valid
        graph."""
        self.G.add_node(label="d", parents=[0], children=[2])
        self.assertTrue(self.G.is_well_formed())
        self.G.add_node(label="e", parents=[0], children=[1])
        self.assertTrue(self.G.is_well_formed())

    def test_is_well_formed_adding_input_nodes_open_digraph(self):
        self.G.add_input_node(0)
        self.assertTrue(self.G.is_well_formed())

    def test_is_well_formed_adding_output_nodes_and_removing_node_open_digraph(self):
        id = self.G.add_output_node(2)
        self.assertTrue(self.G.is_well_formed())
        self.G.remove_node_by_id(id)
        self.assertTrue(self.G.is_well_formed())

    def test_is_well_formed_create_example_from_scratch(self):
        G0 = open_digraph.empty()
        self.assertTrue(G0.is_well_formed())
        a = G0.add_node(label='a')
        self.assertTrue(G0.is_well_formed())
        b = G0.add_node(label='b')
        self.assertTrue(G0.is_well_formed())
        G0.add_edge(a, b)
        self.assertTrue(G0.is_well_formed())
        c = G0.add_node(label='c')
        self.assertTrue(G0.is_well_formed())
        G0.add_edge(a, c)
        self.assertTrue(G0.is_well_formed())
        G0.add_edge(b, c)
        self.assertTrue(G0.is_well_formed())
        G0.add_edge(b, c)
        self.assertTrue(G0.is_well_formed())
        G0.add_input_node(a)
        self.assertTrue(G0.is_well_formed())
        G0.add_input_node(a)
        self.assertTrue(G0.is_well_formed())
        G0.add_output_node(b)
        self.assertTrue(G0.is_well_formed())
        G0.add_output_node(c)
        self.assertTrue(G0.is_well_formed())
        self.assertEqual(str(G0), str(self.G))

    def test_cyclic_graphs_are_cyclic_open_digraph(self):
        self.assertTrue(self.G2.is_cyclic())

    @given(random_well_formed_open_digraph_strategy(form='DAG'))
    def test_DAGs_are_acyclic_open_digraph(self, graph):
        self.assertFalse(graph.is_cyclic())

    @given(open_digraph_strategy(), st.integers())
    def test_shift_indices_open_digraph(self, graph, n):
        original = graph.copy()
        graph.shift_indices(n)
        for old in original.get_node_ids():
            self.assertIn(old + n, graph.get_node_ids())
            old_node = original.get_node_by_id(old)
            new_node = graph.get_node_by_id(old + n)
            for old_parent in old_node.get_parent_ids():
                self.assertIn(old_parent + n, new_node.get_parent_ids())
            for old_child in old_node.get_children_ids():
                self.assertIn(old_child + n, new_node.get_children_ids())
        for old in original.get_input_ids():
            self.assertIn(old + n, graph.get_input_ids())
        for old in original.get_output_ids():
            self.assertIn(old + n, graph.get_output_ids())

    @given(open_digraph_strategy(), open_digraph_strategy())
    def test_separate_indices_open_digraph(self, g, h):
        g.separate_indices(h)
        for old in h.get_node_ids():
            self.assertNotIn(old, g.get_node_ids())
        for old in h.get_input_ids():
            self.assertNotIn(old, g.get_input_ids())
        for old in h.get_output_ids():
            self.assertNotIn(old, g.get_output_ids())

    def test_fusion_open_digraph(self):
        self.assertRaises(ValueError, self.G.fusion, 0, 13)

        len_before_fusion = len(self.G2.get_node_ids())
        id_fusion = self.G2.fusion(0, 1, "node_fusion")

        self.assertTrue(self.G2.is_well_formed())
        self.assertTrue(self.G2.get_node_by_id(id_fusion).get_label(), "node_fusion") 

        self.assertEqual(len_before_fusion-1, len(self.G2.get_node_ids()))
        self.assertEqual(3, len(self.G2.get_node_by_id(id_fusion).get_parent_ids()))
        self.assertEqual(2, len(self.G2.get_node_by_id(id_fusion).get_children_ids()))

        self.assertIn(id_fusion, self.G2.get_nodes_ids())
        self.assertIn(id_fusion, self.G2.get_node_by_id(2).get_children_ids())
        self.assertIn(2, self.G2.get_node_by_id(id_fusion).get_children_ids())

