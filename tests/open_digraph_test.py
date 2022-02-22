from modules.node import node
from modules.open_digraph import open_digraph
import numpy as np
import pydot
import unittest
import sys
import os
from hypothesis import assume
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


@st.composite
def node_strategy(draw, no_parents=True, no_children=True):
    id = draw(st.integers())
    label = draw(st.text())
    if no_parents:
        parents_min_size = 0
    else:
        parents_min_size = 1
    if no_children:
        children_min_size = 0
    else:
        children_min_size = 1
    parents = draw(st.dictionaries(st.integers(), st.integers(min_value=1), min_size=parents_min_size))
    children = draw(st.dictionaries(st.integers(), st.integers(min_value=1), min_size=children_min_size))
    return node(id, label, parents, children)


@st.composite
def open_digraph_strategy(draw):
    nodes = draw(st.lists(node_strategy()))
    io_num = draw(st.integers(min_value=0, max_value=len(nodes)))
    input_num = draw(st.integers(min_value=0, max_value=io_num))
    io_ids = draw(st.permutations([node.get_id() for node in nodes]).map(lambda x: x[:io_num]))
    input_ids = io_ids[:input_num]
    output_ids = io_ids[input_num+1:]
    return open_digraph(input_ids, output_ids, nodes)

@st.composite
def random_well_formed_open_digraph_strategy(draw, inputs=True, outputs=True, form=None):
    if form == None:
        form = draw(st.sampled_from(['free', 'loop-free', 'undirected', 'loop-free undirected', 'oriented', 'DAG']))
    n = draw(st.integers(min_value=0, max_value=100))
    bound = draw(st.integers(min_value=0))
    if inputs:
        inputs = draw(st.integers(min_value=0, max_value=n/2))
    else:
        inputs = 0
    if outputs:
        outputs = draw(st.integers(min_value=0, max_value=n/2))
    else:
        outputs = 0
    graph = open_digraph.random(n, bound, inputs, outputs, form)
    assume(graph.is_well_formed())
    return graph


class Open_DigraphTest(unittest.TestCase):

    def setUp(self):
        self.n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
        self.n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
        self.n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})

        self.i0 = node(3, 'i0', {}, {0: 1})
        self.i1 = node(4, 'i1', {}, {0: 1})

        self.o0 = node(5, 'o0', {1: 1}, {})
        self.o1 = node(6, 'o1', {2: 1}, {})

        self.G = open_digraph([3, 4], [5, 6], [self.n0, self.n1, self.n2,
                                               self.i0, self.i1, self.o0,
                                               self.o1])

        self.n0_2 = node(0, "v0", {3: 1}, {1: 1, 2: 1})
        self.n1_2 = node(1, "v1", {0: 1}, {3: 1, 4: 2})
        self.n2_2 = node(2, "v2", {0: 1}, {3: 2})
        self.n3_2 = node(3, "v3", {1: 1, 2: 2}, {0: 1, 4: 1})
        self.n4_2 = node(4, "v4", {}, {1: 2, 3: 1})

        self.G2 = open_digraph([], [],
                               [self.n0_2, self.n1_2, self.n2_2, self.n3_2, self.n4_2])
        self.M_G2 = [[0, 1, 1, 0, 0],
                     [0, 0, 0, 1, 2],
                     [0, 0, 0, 2, 0],
                     [1, 0, 0, 0, 1],
                     [0, 2, 0, 1, 0]]

        self.n, self.bound = 10, 15
        self.free_graph = open_digraph.random(self.n, self.bound, form="free")
        self.loop_free_graph = open_digraph.random(self.n, self.bound, form="loop-free")
        self.undirect_graph = open_digraph.random(self.n, self.bound, form="undirected")
        self.loop_free_undirect_graph = open_digraph.random(self.n, self.bound, form="loop-free undirected")
        self.oriented_graph = open_digraph.random(self.n, self.bound, form="oriented")
        self.dag_graph = open_digraph.random(self.n, self.bound, form="DAG")

        self.free_graph_matrix = np.asarray(self.free_graph.adjacency_matrix())
        self.loop_free_graph_matrix = np.asarray(self.loop_free_graph.adjacency_matrix())
        self.undirect_graph_matrix = np.asarray(self.undirect_graph.adjacency_matrix())
        self.loop_free_undirect_graph_matrix = np.asarray(self.loop_free_undirect_graph.adjacency_matrix())
        self.oriented_graph_matrix = np.asarray(self.oriented_graph.adjacency_matrix())
        self.dag_graph_matrix = np.asarray(self.dag_graph.adjacency_matrix())

    @given(open_digraph_strategy())
    def test_copy_open_digraph(self, graph):
        """Test the copy method of open_digraph class."""
        self.assertIsNot(graph.copy(), graph)

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

    @given(open_digraph_strategy())
    def test_new_id_open_digraph(self, graph):
        """Test new_id method."""
        self.assertNotIn(graph.new_id(), graph.get_node_ids())

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

    def test_node_dict_open_digraph(self):
        uniq_dict_1 = open_digraph.node_dict(self.G)
        uniq_dict_2 = open_digraph.node_dict(self.G2)
        self.assertEqual(len(uniq_dict_1), len(set(uniq_dict_1.values())))
        self.assertEqual(len(uniq_dict_2), len(set(uniq_dict_2.values())))

    def test_random_shape_open_digraph(self):
        self.assertEqual((self.n, self.n, ), self.free_graph_matrix.shape)
        self.assertEqual((self.n, self.n, ), self.loop_free_graph_matrix.shape)
        self.assertEqual((self.n, self.n, ), self.undirect_graph_matrix.shape)
        self.assertEqual((self.n, self.n, ), self.loop_free_undirect_graph_matrix.shape)
        self.assertEqual((self.n, self.n, ), self.oriented_graph_matrix.shape)
        self.assertEqual((self.n, self.n, ), self.dag_graph_matrix.shape)

    def test_random_bound_open_digraph(self):
        self.assertTrue(np.asarray(
            [self.free_graph_matrix[i] <= self.bound for i in range(self.n)]).all())

        self.assertTrue(np.asarray(
            [self.loop_free_graph_matrix[i] <= self.bound for i in range(self.n)]).all())

        self.assertTrue(np.asarray(
            [self.undirect_graph_matrix[i] <= self.bound for i in range(self.n)]).all())

        self.assertTrue(np.asarray(
            [self.loop_free_undirect_graph_matrix[i] <= self.bound for i in range(self.n)]).all())

        self.assertTrue(np.asarray(
            [self.oriented_graph_matrix[i] <= self.bound for i in range(self.n)]).all())

        self.assertTrue(np.asarray(
            [self.dag_graph_matrix[i] <= self.bound for i in range(self.n)]).all())
    

    def test_random_loop(self):
        self.assertTrue((self.loop_free_graph_matrix.diagonal() == 0).all())
        self.assertTrue((self.loop_free_undirect_graph_matrix.diagonal() == 0).all())

    def test_random_loop_free_undirect(self):
        graph = self.loop_free_undirect_graph
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_children_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_child_multiplicity(node_id))
    
    def test_random_undirect(self):
        graph = self.undirect_graph
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertIn(node_id, child.get_children_ids())
                self.assertEqual(node.get_child_multiplicity(child_id), child.get_child_multiplicity(node_id))
    
    def test_random_oriented(self):
        graph = self.oriented_graph
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertNotIn(node_id, child.get_children_ids())

    def test_random_DAG_open_digraph(self):
        """
        Pas suffisant
        """
        graph = self.dag_graph
        for node_id in graph.get_node_ids():
            node = graph.get_node_by_id(node_id)
            for child_id in node.get_children_ids():
                child = graph.get_node_by_id(child_id)
                self.assertNotIn(node_id, child.get_children_ids())

    def test_save_as_dot_file(self):
        dot_file_path = "test_as_save_dot_file.dot"
        self.G.save_as_dot_file(dot_file_path)
        pydot.graph_from_dot_file(dot_file_path)

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

    def test_cyclic_graphs_are_cyclic_open_digraph(self):
        self.assertTrue(self.G2.is_cyclic())

    def test_acyclic_graphs_are_acyclic_open_digraph(self):
        self.assertFalse(self.dag_graph.is_cyclic())

    @given(open_digraph_strategy())
    def test_min_id_open_digraph(self, graph):
        if len(graph.get_id_node_map()) > 0:
            self.assertEqual(graph.min_id(), min(graph.get_node_ids()))
        else:
            self.assertRaises(ValueError, graph.min_id)
            
    @given(open_digraph_strategy())
    def test_max_id_open_digraph(self, graph):
        if len(graph.get_id_node_map()) > 0:
            self.assertEqual(graph.max_id(), max(graph.get_node_ids()))
        else:
            self.assertRaises(ValueError, graph.min_id)
            
    @given(open_digraph_strategy(), st.integers())
    def test_shift_indices_open_digraph(self, graph, n):
        if len(graph.get_id_node_map()) > 0:
            m = graph.min_id()
            M = graph.max_id()
            graph.shift_indices(n)
            ids = np.asarray(graph.get_node_ids())
            self.assertTrue(np.all(ids >= np.full(ids.shape, m + n)))
            self.assertTrue(np.all(ids <= np.full(ids.shape, M + n)))
        else:
            self.assertRaises(ValueError, graph.shift_indices, n)

    @given(open_digraph_strategy(), st.lists(open_digraph_strategy()))
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

    @given(open_digraph_strategy(), st.lists(open_digraph_strategy()))
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

    @given(open_digraph_strategy(), open_digraph_strategy())
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
            self.assertEqual(len(graph.get_id_node_map()), nodes1 + nodes2)
        else:
            self.assertRaises(ValueError, graph.icompose, g)

    @given(open_digraph_strategy(), open_digraph_strategy())
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
            self.assertEqual(len(new.get_id_node_map()), nodes1 + nodes2)
        else:
            self.assertRaises(ValueError, graph.compose, g)

    @given(open_digraph_strategy())
    def test_connected_components_open_digraph(self, graph):
        n, d = graph.connected_components()
        ids = graph.get_node_ids()
        self.assertGreaterEqual(n, 0)
        for k, v in d.items():
            self.assertIn(k, ids)
            self.assertLessEqual(v, n)
