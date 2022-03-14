from modules.open_digraph import open_digraph
from tests.strategy import open_digraph_strategy
import unittest
import pydot
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_display_mx_test(unittest.TestCase):
    @given(open_digraph_strategy())
    def test_save_as_dot_file(self, graph):
        dot_file_path = "test_as_save_dot_file.dot"
        graph.save_as_dot_file(dot_file_path)
        pydot.graph_from_dot_file(dot_file_path)
        os.remove(dot_file_path)

    def test_from_dot_file(self):
        dot_file_content = """digraph G {
v0 [label="&"];
v1 [label="~"];
v4 [label="|"];
v0 -> v1 -> v2;
v0 -> v3;
v2 -> v3;
v2 -> v3;
v3 -> v4;
v2 -> v4;
}
"""
        dot_file_path = "test_from_dot_file.dot"
        with open(dot_file_path, 'w') as dot_file:
            print(dot_file_content, file=dot_file)
        graph = open_digraph.from_dot_file(dot_file_path)
        self.assertTrue(graph.is_well_formed())
        os.remove(dot_file_path)
