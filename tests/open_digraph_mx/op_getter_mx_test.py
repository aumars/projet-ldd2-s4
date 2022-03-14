from tests.strategy import open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_getter_mx_test(unittest.TestCase):
    @given(open_digraph_strategy())
    def test_get_input_ids_open_digraph(self, graph):
        """Test the get_input_ids method."""
        self.assertEqual(graph.get_input_ids(), graph.inputs)

    @given(open_digraph_strategy())
    def test_get_output_ids_open_digraph(self, graph):
        """Test the get_output_ids method."""
        self.assertEqual(graph.get_output_ids(), graph.outputs)

    @given(open_digraph_strategy())
    def test_get_id_node_map_open_digraph(self, graph):
        """Test the get_id_node_map method."""
        self.assertEqual(graph.get_id_node_map(), graph.nodes)

    @given(open_digraph_strategy())
    def test_get_nodes_open_digraph(self, graph):
        """Test the get_nodes method."""
        self.assertCountEqual(graph.get_nodes(), graph.nodes.values())

    @given(open_digraph_strategy())
    def test_get_node_ids_open_digraph(self, graph):
        """Test the get_ids method."""
        self.assertCountEqual(graph.get_node_ids(), graph.nodes.keys())

    @given(open_digraph_strategy(), st.integers())
    def test_get_node_by_id_open_digraph(self, graph, id):
        """Test the get_node_by_id method."""
        if id in graph.get_node_ids():
            self.assertEqual(graph.get_node_by_id(id), graph.get_id_node_map()[id])
        else:
            self.assertRaises(ValueError, graph.get_node_by_id, id)

    @given(open_digraph_strategy(), st.lists(st.integers()))
    def test_get_nodes_by_ids_open_digraph(self, graph, id_list):
        """Test the get_nodes_by_ids method."""
        if set(id_list).issubset(graph.get_node_ids()):
            self.assertCountEqual(graph.get_nodes_by_ids(id_list), list(map(graph.get_id_node_map().get, id_list)))
        else:
            self.assertRaises(ValueError, graph.get_nodes_by_ids, id_list)
