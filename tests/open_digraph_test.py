from modules.node import node
from modules.open_digraph import open_digraph
import unittest
import sys
import os
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
                     [0]*5]

    def test_init_open_digraph(self):
        """Test the constructor."""
        self.assertIsInstance(self.G, open_digraph)

    def test_copy_open_digraph(self):
        """Test the copy method of open_digraph class."""
        self.assertIsNot(self.G.copy(), self.G)

    def test_get_input_ids_open_digraph(self):
        """Test the get_input_ids method."""
        self.assertEqual(self.G.get_input_ids(), [3, 4])

    def test_get_output_ids_open_digraph(self):
        """Test the get_output_ids method."""
        self.assertEqual(self.G.get_output_ids(), [5, 6])

    def test_get_id_node_map_open_digraph(self):
        """Test the get_id_node_map method."""
        self.assertEqual(self.G.get_id_node_map(),
                         {0: self.n0, 1: self.n1, 2: self.n2, 3: self.i0,
                          4: self.i1, 5: self.o0, 6: self.o1})

    def test_get_nodes_open_digraph(self):
        """Test the get_nodes method."""
        self.assertEqual(self.G.get_nodes(), [self.n0, self.n1, self.n2,
                                              self.i0, self.i1, self.o0,
                                              self.o1])

    def test_get_node_ids_open_digraph(self):
        """Test the get_ids method."""
        self.assertEqual(self.G.get_node_ids(), [0, 1, 2, 3, 4, 5, 6])

    def test_get_node_by_id_existing_id_open_digraph(self):
        """Test the get_node_by_id method with existing ID."""
        self.assertEqual(self.G.get_node_by_id(0), self.n0)

    def test_get_node_by_id_nonexistant_id_open_digraph(self):
        """Test the get_node_by_id method with nonexistant ID."""
        self.assertRaises(ValueError, self.G.get_node_by_id, -1)

    def test_get_nodes_by_ids_existing_ids_open_digraph(self):
        """Test the get_nodes_by_ids method with existing IDs."""
        self.assertEqual(self.G.get_nodes_by_ids([0, 1]), [self.n0, self.n1])

    def test_get_nodes_by_ids_nonexistant_id_open_digraph(self):
        """Test the get_nodes_by_ids method with a nonexistant ID."""
        self.assertRaises(ValueError, self.G.get_nodes_by_ids, [0, -1])

    def test_set_input_ids_open_digraph(self):
        """Test the set_input_ids method with valid IDs."""
        self.G.set_input_ids([0, 1])
        self.assertEqual(self.G.get_input_ids(), [0, 1])

    def test_set_input_ids_negative_ids_open_digraph(self):
        """Test the set_input_ids method with negative IDs."""
        self.G.set_input_ids([0, -1])
        self.assertEqual(self.G.get_input_ids(), [0, -1])

    def test_set_input_ids_duplicate_ids_open_digraph(self):
        """Test the set_input_ids method with duplicate IDs."""
        self.G.set_input_ids([0, 0, 1])
        self.assertEqual(self.G.get_input_ids(), [0, 1])

    def test_set_output_ids_open_digraph(self):
        """Test the set_output_ids method with valid IDs."""
        self.G.set_output_ids([0, 1])
        self.assertEqual(self.G.get_output_ids(), [0, 1])

    def test_set_output_ids_negative_ids_open_digraph(self):
        """Test the set_output_ids method with negative IDs."""
        self.G.set_output_ids([0, -1])
        self.assertEqual(self.G.get_output_ids(), [0, -1])

    def test_set_output_ids_duplicate_ids_open_digraph(self):
        """Test the set_output_ids method with duplicate IDs."""
        self.G.set_output_ids([0, 0, 1])
        self.assertEqual(self.G.get_output_ids(), [0, 1])

    def test_add_input_id_open_unused_digraph(self):
        """Test add_input_id with unused ID"""
        self.G.add_input_id(7)
        self.assertIn(7, self.G.get_input_ids())

    def test_add_input_id_existing_input_id_open_digraph(self):
        """Test add_input_id with existing input ID"""
        self.G.add_input_id(3)
        self.assertIn(3, self.G.get_input_ids())

    def test_add_input_id_existing_output_id_open_digraph(self):
        """Test add_input_id with existing output ID"""
        self.assertRaises(ValueError, self.G.add_input_id, 5)

    def test_add_input_id_existing_internal_id_open_digraph(self):
        """Test add_input_id with existing internal ID (neither input nor
        output)"""
        self.assertRaises(ValueError, self.G.add_input_id, 0)

    def test_add_output_id_open_unused_digraph(self):
        """Test add_output_id with unused ID"""
        self.G.add_output_id(7)
        self.assertIn(7, self.G.get_output_ids())

    def test_add_output_id_existing_output_id_open_digraph(self):
        """Test add_output_id with existing output ID"""
        self.G.add_output_id(5)
        self.assertIn(5, self.G.get_output_ids())

    def test_add_output_id_existing_input_id_open_digraph(self):
        """Test add_output_id with existing input ID"""
        self.assertRaises(ValueError, self.G.add_output_id, 3)

    def test_add_output_id_existing_internal_id_open_digraph(self):
        """Test add_output_id with existing internal ID (neither input nor
        output)"""
        self.assertRaises(ValueError, self.G.add_output_id, 0)

    def test_new_id_open_digraph(self):
        """Test new_id method."""
        self.assertNotIn(self.G.new_id(), self.G.get_node_ids())

    def test_add_edge_between_two_valid_nodes_open_digraph(self):
        """Test add_edge method between two valid nodes."""
        self.G.add_edge(2, 0)
        self.assertEqual(self.G.get_node_by_id(2).get_child_multiplicity(0), 1)
        self.assertEqual(self.G.get_node_by_id(
            0).get_parent_multiplicity(2), 1)

    def test_add_edge_from_valid_node_to_input_node_open_digraph(self):
        """Test add_edge method from valid node to input node."""
        self.assertRaises(ValueError, self.G.add_edge, 2, 3)

    def test_add_edge_from_output_node_to_valid_node_open_digraph(self):
        """Test add_edge method from output node to valid node."""
        self.assertRaises(ValueError, self.G.add_edge, 5, 0)

    def test_add_edge_from_valid_node_to_nonexistant_node_open_digraph(self):
        """Test add_edge method from valid node to nonexistant node."""
        self.assertRaises(ValueError, self.G.add_edge, 0, 7)

    def test_add_node_valid_nodes_open_digraph(self):
        """Test add_node method by adding a node with an edge from ID 3
        and an edge to ID 1."""
        node_cpt = len(self.G.get_nodes())
        id = self.G.add_node(parents=[3], children=[1])
        self.assertEqual(len(self.G.get_nodes()), node_cpt + 1)
        self.assertIn(id, self.G.get_node_ids())
        self.assertEqual(self.G.get_node_by_id(
            id).get_parent_multiplicity(3), 1)
        self.assertEqual(self.G.get_node_by_id(
            3).get_child_multiplicity(id), 1)
        self.assertEqual(self.G.get_node_by_id(
            id).get_child_multiplicity(1), 1)
        self.assertEqual(self.G.get_node_by_id(
            1).get_parent_multiplicity(id), 1)

    def test_add_node_nonexistant_parent_open_digraph(self):
        """Test add_node method with a nonexistant parent."""
        self.assertRaises(ValueError, self.G.add_node,
                          parents=[-1], children=[1])

    def test_add_node_output_parent_open_digraph(self):
        """Test add_node method with a output parent."""
        self.assertRaises(ValueError, self.G.add_node,
                          parents=[5], children=[1])

    def test_add_node_input_child_open_digraph(self):
        """Test add_node method with a input child."""
        self.assertRaises(ValueError, self.G.add_node,
                          parents=[0], children=[3])

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

    # def test_graph_from_adjacency_matrix(self):
    #     G = open_digraph.graph_from_adjacency_matrix(self.M_G2)
    #     print("\nAffichage Graphe G2 original :\n", self.G2)
    #     print("\nAffichage Graphe G construit :\n", G)

    def test_adjacency_matrix(self):
        self.assertListEqual(self.G2.adjacency_matrix(), self.M_G2)

    def test_node_dict(self):
        uniq_dict_1 = open_digraph.node_dict(self.G)
        uniq_dict_2 = open_digraph.node_dict(self.G2)
        self.assertEqual(len(uniq_dict_1), len(set(uniq_dict_1.values())))
        self.assertEqual(len(uniq_dict_2), len(set(uniq_dict_2.values())))
