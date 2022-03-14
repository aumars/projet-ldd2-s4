from modules.node import node
from modules.open_digraph import open_digraph
from tests.strategy import open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_modify_mx_test(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})

        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})

        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})

        self.G = open_digraph([3, 4], [5, 6], [self.n0, self.n1, self.n2, self.i0, self.i1, self.o0, self.o1])
        
    @given(open_digraph_strategy(), st.integers())
    def test_add_input_id_open_digraph(self, graph, id):
        """Test add_input_id method."""
        if id in graph.get_node_ids() and id not in graph.get_output_ids() and graph.get_node_by_id(id).get_parent_ids() == [] and len(graph.get_node_by_id(id).get_children_ids()) == 1:
            graph.add_input_id(id)
            self.assertIn(id, graph.get_input_ids())
        else:
            self.assertRaises(ValueError, graph.add_input_id, id)

    @given(open_digraph_strategy(), st.integers())
    def test_add_output_id_open_digraph(self, graph, id):
        """Test add_output_id method."""
        if id in graph.get_node_ids() and id not in graph.get_input_ids() and graph.get_node_by_id(id).get_children_ids() == [] and len(graph.get_node_by_id(id).get_parent_ids()) == 1:
            graph.add_output_id(id)
            self.assertIn(id, graph.get_output_ids())
        else:
            self.assertRaises(ValueError, graph.add_output_id, id)

    @given(open_digraph_strategy(), st.integers(), st.integers())
    def test_add_edge_open_digraph(self, graph, src, tgt):
        """Test add_edge method."""
        if src in graph.get_node_ids() and tgt in graph.get_node_ids() \
           and src not in graph.get_output_ids() and tgt not in graph.get_input_ids():
            c = graph.get_node_by_id(src).get_child_multiplicity(tgt)
            p = graph.get_node_by_id(tgt).get_parent_multiplicity(src)
            graph.add_edge(src, tgt)
            self.assertEqual(graph.get_node_by_id(src).get_child_multiplicity(tgt), c + 1)
            self.assertEqual(graph.get_node_by_id(tgt).get_parent_multiplicity(src), p + 1)
        else:
            self.assertRaises(ValueError, graph.add_edge, src, tgt)

    @given(open_digraph_strategy(), st.text(), st.lists(st.integers()), st.lists(st.integers()))
    def test_add_node_open_digraph(self, graph, label, parents, children):
        """Test add_node method."""
        P, C = set(parents), set(children)
        N, O, I = set(graph.get_id_node_map()), set(graph.get_output_ids()), set(graph.get_input_ids())
        if P.issubset(N) and C.issubset(N) and P.intersection(O) == set() and C.intersection(I) == set():
            node_num = len(graph.get_nodes())
            id = graph.add_node(parents, children)
            node = graph.get_node_by_id(id)
            self.assertEqual(len(graph.get_nodes()), node_num + 1)
            self.assertIn(id, graph.get_node_ids())
            for parent in parents:
                self.assertEqual(node.get_parent_multiplicity(parent), 1)
            for child in children:
                self.assertEqual(node.get_child_multiplicity(child), 1)
        else:
            self.assertRaises(ValueError, graph.add_node, label, parents, children)

    def test_add_input_node_open_digraph(self):
        id = self.G.add_input_node(0)
        self.assertIn(id, self.G.get_input_ids())
        self.assertRaises(ValueError, self.G.add_input_node, 3)
        self.assertRaises(ValueError, self.G.add_input_node, 5)

    def test_add_output_node_open_digraph(self):
        id = self.G.add_output_node(0)
        self.assertIn(id, self.G.get_output_ids())
        self.assertRaises(ValueError, self.G.add_output_node, 3)
        self.assertRaises(ValueError, self.G.add_output_node, 5)

    def test_remove_edges_existing_edges_open_digraph(self):
        """Test remove_edges method with existing edges."""
        self.G.remove_edges((0, 1), (1, 2), (2, 6))
        self.assertNotIn(1, self.G.get_node_by_id(0).get_children_ids())
        self.assertNotIn(0, self.G.get_node_by_id(1).get_parent_ids())
        self.assertEqual(self.G.get_node_by_id(1).get_child_multiplicity(2), 1)
        self.assertEqual(self.G.get_node_by_id(
            2).get_parent_multiplicity(1), 1)
        self.assertNotIn(6, self.G.get_node_by_id(2).get_children_ids())
        self.assertNotIn(2, self.G.get_node_by_id(6).get_parent_ids())

    def test_remove_edges_nonexistant_edges_open_digraph(self):
        """Test remove_edges method with nonexistant edges."""
        self.G.remove_edges((1, 0))
        self.assertNotIn(0, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(0).get_parent_ids())

    def test_remove_edges_existing_and_nonexistant_edges_open_digraph(self):
        """Test remove_edges method with existing and nonexistant edges."""
        self.G.remove_edges((3, 0), (4, 0), (1, 0))
        self.assertNotIn(0, self.G.get_node_by_id(3).get_children_ids())
        self.assertNotIn(3, self.G.get_node_by_id(0).get_parent_ids())
        self.assertNotIn(0, self.G.get_node_by_id(4).get_children_ids())
        self.assertNotIn(4, self.G.get_node_by_id(0).get_parent_ids())
        self.assertNotIn(0, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(0).get_parent_ids())

    def test_remove_edges_nonexistant_node_open_digraph(self):
        """Test remove_edges method with nonexistant node."""
        self.G.remove_edges((1, 7))
        self.assertNotIn(7, self.G.get_node_by_id(1).get_children_ids())
        self.assertRaises(ValueError, self.G.get_node_by_id, 7)

    def test_remove_parallel_edges_existing_edges_open_digraph(self):
        """Test remove_parallel_edges method with exising edges."""
        self.G.remove_parallel_edges((1, 0), (1, 2))
        self.assertNotIn(0, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(0).get_parent_ids())
        self.assertNotIn(2, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(2).get_parent_ids())

    def test_remove_parallel_edges_nonexistant_edges_open_digraph(self):
        """Test remove_parallel_edges method with nonexistant edges."""
        self.G.remove_parallel_edges((0, 5))
        self.assertNotIn(5, self.G.get_node_by_id(0).get_children_ids())
        self.assertNotIn(0, self.G.get_node_by_id(5).get_parent_ids())

    def test_remove_parallel_edges_existing_and_nonexistant_edges_open_digraph(self):
        """Test remove_parallel_edges method with existing and nonexistant edges."""
        self.G.remove_parallel_edges((1, 0), (1, 2), (0, 5))
        self.assertNotIn(0, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(0).get_parent_ids())
        self.assertNotIn(2, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(1, self.G.get_node_by_id(2).get_parent_ids())
        self.assertNotIn(5, self.G.get_node_by_id(0).get_children_ids())
        self.assertNotIn(0, self.G.get_node_by_id(5).get_parent_ids())

    def test_remove_parallel_edges_nonexistant_node_open_digraph(self):
        """Test remove_parallel_edges method with nonexistant node."""
        self.G.remove_parallel_edges((1, 7))
        self.assertNotIn(7, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(7, self.G.get_node_ids())

    def test_remove_nodes_by_id_existing_nodes_open_digraph(self):
        """Test remove_nodes_by_id method with existing nodes, including an
        output node."""
        self.G.remove_nodes_by_id([2, 6])
        self.assertNotIn(2, self.G.get_node_by_id(0).get_children_ids())
        self.assertNotIn(2, self.G.get_node_by_id(1).get_children_ids())
        self.assertNotIn(2, self.G.get_node_ids())
        self.assertNotIn(6, self.G.get_node_ids())
        self.assertNotIn(6, self.G.get_output_ids())

    def test_remove_nodes_by_id_nonexistant_node_open_digraph(self):
        """Test remove_nodes_by_id method with nonexistant node."""
        self.G.remove_nodes_by_id([19])
        self.assertNotIn(19, self.G.get_node_ids())
