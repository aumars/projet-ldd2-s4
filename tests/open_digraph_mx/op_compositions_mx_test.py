from tests.strategy import random_well_formed_open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_compositions_mx_test(unittest.TestCase):
    @given(random_well_formed_open_digraph_strategy(), st.lists(random_well_formed_open_digraph_strategy()))
    def test_iparallel_open_digraph(self, graph, l):
        inputs1 = len(graph.get_input_ids())
        outputs1 = len(graph.get_output_ids())
        nodes1 = len(graph.get_id_node_map())
        inputs2 = sum([len(g.get_input_ids()) for g in l])
        outputs2 = sum([len(g.get_output_ids()) for g in l])
        nodes2 = sum([len(g.get_id_node_map()) for g in l])
        graph.iparallel(l)
        self.assertEqual(len(graph.get_input_ids()), inputs1 + inputs2)
        self.assertEqual(len(graph.get_output_ids()), outputs1 + outputs2)
        self.assertEqual(len(graph.get_id_node_map()), nodes1 + nodes2)

    @given(random_well_formed_open_digraph_strategy(), st.lists(random_well_formed_open_digraph_strategy()))
    def test_parallel_open_digraph(self, graph, l):
        inputs1 = len(graph.get_input_ids())
        outputs1 = len(graph.get_output_ids())
        nodes1 = len(graph.get_id_node_map())
        inputs2 = sum([len(g.get_input_ids()) for g in l])
        outputs2 = sum([len(g.get_output_ids()) for g in l])
        nodes2 = sum([len(g.get_id_node_map()) for g in l])
        new = graph.parallel(l)
        self.assertEqual(len(new.get_input_ids()), inputs1 + inputs2)
        self.assertEqual(len(new.get_output_ids()), outputs1 + outputs2)
        self.assertEqual(len(new.get_id_node_map()), nodes1 + nodes2)

    @given(random_well_formed_open_digraph_strategy(), random_well_formed_open_digraph_strategy())
    def test_icompose_open_digraph(self, graph, g):
        inputs1 = len(graph.get_input_ids())
        outputs1 = len(graph.get_output_ids())
        nodes1 = len(graph.get_id_node_map())
        inputs2 = len(g.get_input_ids())
        outputs2 = len(g.get_output_ids())
        nodes2 = len(g.get_id_node_map())
        if outputs1 == inputs2:
            graph.icompose(g)
            self.assertEqual(len(graph.get_input_ids()), inputs1)
            self.assertEqual(len(graph.get_output_ids()), outputs2)
            self.assertEqual(len(graph.get_id_node_map()), nodes1 + nodes2 - outputs1)
        else:
            self.assertRaises(ValueError, graph.icompose, g)

    @given(random_well_formed_open_digraph_strategy(), random_well_formed_open_digraph_strategy())
    def test_compose_open_digraph(self, graph, g):
        inputs1 = len(graph.get_input_ids())
        outputs1 = len(graph.get_output_ids())
        nodes1 = len(graph.get_id_node_map())
        inputs2 = len(g.get_input_ids())
        outputs2 = len(g.get_output_ids())
        nodes2 = len(g.get_id_node_map())
        if outputs1 == inputs2:
            new = graph.compose(g)
            self.assertEqual(len(new.get_input_ids()), inputs1)
            self.assertEqual(len(new.get_output_ids()), outputs2)
            self.assertEqual(len(new.get_id_node_map()), nodes1 + nodes2 - outputs1)
        else:
            self.assertRaises(ValueError, graph.compose, g)
