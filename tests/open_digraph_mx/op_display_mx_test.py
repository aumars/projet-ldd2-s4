from modules.open_digraph import open_digraph
from tests.strategy import random_well_formed_open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_display_mx_test(unittest.TestCase):
    @given(random_well_formed_open_digraph_strategy())
    def test_dot_file(self, graph):
        dot_file_path = "test_as_save_dot_file.dot"
        graph.save_as_dot_file(dot_file_path)
        graph2 = open_digraph.from_dot_file(dot_file_path)
        self.assertTrue(graph2.is_well_formed())
        os.remove(dot_file_path)
