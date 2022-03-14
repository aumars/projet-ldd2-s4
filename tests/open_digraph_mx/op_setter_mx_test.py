from tests.strategy import open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_setter_mx_test(unittest.TestCase):
    @given(open_digraph_strategy(), st.lists(st.integers()))
    def test_set_input_ids_open_digraph(self, graph, input_ids):
        """Test the set_input_ids method."""
        graph.set_input_ids(input_ids)
        self.assertEqual(set(graph.get_input_ids()), set(input_ids))

    @given(open_digraph_strategy(), st.lists(st.integers()))
    def test_set_output_ids_open_digraph(self, graph, output_ids):
        """Test the set_output_ids method."""
        graph.set_output_ids(output_ids)
        self.assertEqual(set(graph.get_output_ids()), set(output_ids))
