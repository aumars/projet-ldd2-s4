from modules.open_digraph import node, open_digraph
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class NodeTest(unittest.TestCase):
    """Tests of the node and open_digraph classes."""

    def setUp(self):
        self.n0 = node(1, '1', {0: 1}, {2: 1})

    def test_init_node(self):
        """Test the init method of node class."""
        self.assertEqual(self.n0.id, 1)
        self.assertEqual(self.n0.label, '1')
        self.assertEqual(self.n0.parents, {0: 1})
        self.assertEqual(self.n0.children, {2: 1})
        self.assertIsInstance(self.n0, node)

    def test_copy_node(self):
        """Test the copy method of node class."""
        self.assertIsNot(self.n0.copy(), self.n0)

    def test_get_id_node(self):
        self.assertEqual(self.n0.get_id(), 1)

    def test_get_label_node(self):
        self.assertEqual(self.n0.get_label(), '1')

    def test_get_parent_ids_node(self):
        self.assertEqual(self.n0.get_parent_ids(), [0])

    def test_get_children_ids_node(self):
        self.assertEqual(self.n0.get_children_ids(), [2])

    def test_set_id_node(self):
        self.n0.set_id(10)
        self.assertEqual(self.n0.get_id(), 10)
        self.n0.set_id(1)
        self.assertEqual(self.n0.get_id(), 1)

    def test_set_label_node(self):
        self.n0.set_label('a')
        self.assertEqual(self.n0.get_label(), 'a')
        self.n0.set_label('b')
        self.assertEqual(self.n0.get_label(), 'b')

    def test_set_parent_ids_node(self):
        self.n0.set_parent_ids([0, 1])
        self.assertEqual(self.n0.get_parent_ids(), [0, 1])

    def test_set_children_ids_node(self):
        self.n0.set_children_ids([0, 1])
        self.assertEqual(self.n0.get_children_ids(), [0, 1])

    def test_add_child_id_node(self):
        """Test the add_child_id method of open_digraph class."""
        self.n0.add_child_id(10)
        self.assertIn(10, self.n0.get_children_ids())
        self.assertNotIn(12, self.n0.get_children_ids())
        self.n0.add_child_id(10)
        self.n0.add_child_id(12)
        self.assertIn(10, self.n0.get_children_ids())
        self.assertIn(12, self.n0.get_children_ids())

    def test_add_parent_id_node(self):
        """Test the add_parent_id method of open_digraph class."""
        self.n0.add_parent_id(10)
        self.assertIn(10, self.n0.get_parent_ids())
        self.assertNotIn(12, self.n0.get_parent_ids())
        self.n0.add_parent_id(10)
        self.n0.add_parent_id(12)
        self.assertIn(10, self.n0.get_parent_ids())
        self.assertIn(12, self.n0.get_parent_ids())


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

    def test_init_open_digraph(self):
        """Test the init method of open_digraph class."""
        self.assertEqual(self.G.inputs, [3, 4])
        self.assertEqual(self.G.outputs, [5, 6])
        self.assertEqual(self.G.nodes, {0: self.n0, 1: self.n1, 2: self.n2,
                                        3: self.i0, 4: self.i1, 5: self.o0,
                                        6: self.o1})

    def test_copy_open_digraph(self):
        """Test the copy method of open_digraph class."""
        self.assertIsNot(self.G.copy(), self.G)

    def test_get_input_ids_open_digraph(self):
        self.assertEqual(self.G.get_input_ids(), [3, 4])

    def test_get_output_ids_open_digraph(self):
        self.assertEqual(self.G.get_output_ids(), [5, 6])

    def test_get_id_node_map_open_digraph(self):
        self.assertEqual(self.G.get_id_node_map(),
                         {0: self.n0, 1: self.n1, 2: self.n2, 3: self.i0,
                          4: self.i1, 5: self.o0, 6: self.o1})

    def test_get_nodes_open_digraph(self):
        self.assertEqual(self.G.get_nodes(), [self.n0, self.n1, self.n2,
                                              self.i0, self.i1, self.o0,
                                              self.o1])

    def test_get_node_ids_open_digraph(self):
        self.assertEqual(self.G.get_node_ids(), [0, 1, 2, 3, 4, 5, 6])

    def test_get_node_by_id_open_digraph(self):
        self.assertEqual(self.G.get_node_by_id(0), self.n0)
        self.assertEqual(self.G.get_node_by_id(3), self.i0)
        self.assertRaises(KeyError, self.G.get_node_by_id, 7)
        self.assertRaises(KeyError, self.G.get_node_by_id, -1)

    def test_get_nodes_by_ids_open_digraph(self):
        self.assertEqual(self.G.get_nodes_by_ids([0, 1]), [self.n0, self.n1])
        self.assertRaises(KeyError, self.G.get_nodes_by_ids, [7, 8])
        self.assertRaises(KeyError, self.G.get_nodes_by_ids, [0, -1])

    def test_set_input_ids_open_digraph(self):
        self.G.set_input_ids([0, 1])
        self.assertEqual(self.G.get_input_ids(), [0, 1])

    def test_set_output_ids_open_digraph(self):
        self.G.set_output_ids([0, 1])
        self.assertEqual(self.G.get_output_ids(), [0, 1])

    def test_add_input_id_open_digraph(self):
        # Pas terminé : un noeud sortant peut être un noeud entrant ?
        # Et un noeud interne ?
        self.G.add_input_id(0)
        self.assertIn(0, self.G.get_input_ids())

    def test_add_output_id_open_digraph(self):
        # Pas terminé : comme le précédent
        self.G.add_output_id(0)
        self.assertIn(0, self.G.get_output_ids())

    def test_new_id_open_digraph(self):
        self.assertNotIn(self.G.new_id(), self.G.get_node_ids())

    def test_add_edge_open_digraph(self):
        # Flèche de C vers A
        self.G.add_edge(2, 0)
        # Un deuxième
        self.G.add_edge(2, 0)
        # 3 est un noeud entrant
        self.assertRaises(ValueError, self.G.add_edge, 0, 3)
        # 5 est un noeud sortant
        self.assertRaises(ValueError, self.G.add_edge, 5, 0)

    def test_add_node_open_digraph(self):
        node_cpt = len(self.G.get_nodes())
        # Ajoute un noeud avec une flèche de 3 et une flèche vers 1
        self.G.add_node(parents=[3], children=[1])
        self.assertEqual(len(self.G.get_nodes()), node_cpt + 1)
        self.assertEqual(len(self.G.get_node_by_id(3).get_children_ids()), 2)
        self.assertEqual(len(self.G.get_node_by_id(1).get_parent_ids()), 2)

        # Un noeud ne peut pas avoir un noeud sortant comme parent
        self.assertRaises(ValueError, self.G.add_node, parents=[5])
        # Un noeud ne peut pas avoir un noeud entrant comme enfant
        self.assertRaises(ValueError, self.G.add_node, children=[4])

if __name__ == '__main__':  # the following code is called only when
    unittest.main()
# precisely this file is run
