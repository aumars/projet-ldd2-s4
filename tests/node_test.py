from modules.node import node
import unittest
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class NodeTest(unittest.TestCase):
    """Tests of the node class."""

    def setUp(self):
        self.n0 = node(1, '1', {0: 1}, {2: 1})
        self.n1 = self.n0.copy()
        self.n2 = node(3, '5', {2: 1}, {})

    def test_init_node(self):
        """Test the constructor."""
        self.assertEqual(self.n0.id, 1)
        self.assertEqual(self.n0.label, '1')
        self.assertEqual(self.n0.parents, {0: 1})
        self.assertEqual(self.n0.children, {2: 1})
        self.assertIsInstance(self.n0, node)

    def test_equal_operator(self):
        """Test the equal operator"""
        self.assertTrue(self.n0 == self.n0)
        self.assertTrue(self.n0 == self.n1)
        self.assertTrue(self.n0 != self.n2)

    def test_copy_node(self):
        """Test the copy method."""
        self.assertIsNot(self.n0.copy(), self.n0)

    def test_get_id_node(self):
        """Test the get_id method."""
        self.assertEqual(self.n0.get_id(), 1)

    def test_get_label_node(self):
        """Test the get_label method."""
        self.assertEqual(self.n0.get_label(), '1')

    def test_get_parent_ids_node(self):
        """Test the get_parents_ids method."""
        self.assertEqual(self.n0.get_parent_ids(), [0])

    def test_get_children_ids_node(self):
        """Test the get_children_ids method."""
        self.assertEqual(self.n0.get_children_ids(), [2])

    def test_get_parent_multiplicity_node(self):
        """Test the get_parent_multiplicity method."""
        self.assertEqual(self.n0.get_parent_multiplicity(0), 1)

    def test_get_parent_multiplicity_nonexistant_id_node(self):
        """Test the get_parent_multiplicity method given an nonexistant ID."""
        self.assertRaises(ValueError, self.n0.get_parent_multiplicity, 1)

    def test_get_child_multiplicity_node(self):
        """Test the get_child_multiplicity method."""
        self.assertEqual(self.n0.get_child_multiplicity(2), 1)

    def test_get_child_multiplicity_nonexistant_id_node(self):
        """Test the get_child_multiplicity method given an nonexistant ID."""
        self.assertRaises(ValueError, self.n0.get_child_multiplicity, 1)

    def test_set_id_node(self):
        """Test the set_id method given a positive integer."""
        self.n0.set_id(10)
        self.assertEqual(self.n0.get_id(), 10)

    def test_set_negative_id_node(self):
        """Test the set_id method given a stricly negative integer."""
        self.n0.set_id(-1)
        self.assertEqual(self.n0.get_id(), -1)

    def test_set_empty_label_node(self):
        """Test the set_label method given an empty string."""
        self.n0.set_label('')
        self.assertEqual(self.n0.get_label(), '')

    def test_set_label_node(self):
        """Test the set_label method given a single character."""
        self.n0.set_label('a')
        self.assertEqual(self.n0.get_label(), 'a')

    def test_set_string_label_node(self):
        """Test the set_label method given a string of multiple characters."""
        self.n0.set_label('aa')
        self.assertEqual(self.n0.get_label(), 'aa')

    def test_set_parent_ids_empty_list_node(self):
        """Test the set_parent_ids method given an empty list."""
        self.n0.set_parent_ids([])
        self.assertEqual(self.n0.get_parent_ids(), [])

    def test_set_parent_ids_node(self):
        """Test the set_parent_ids method given a valid list."""
        self.n0.set_parent_ids([0, 1])
        self.assertIn(0, self.n0.get_parent_ids())
        self.assertIn(1, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(0), 1)
        self.assertEqual(self.n0.get_parent_multiplicity(1), 1)

    def test_set_parent_negative_id_node(self):
        """Test the set_parent_ids method given a list with a strictly negative
        ID."""
        self.n0.set_parent_ids([0, -1])
        self.assertIn(0, self.n0.get_parent_ids())
        self.assertIn(-1, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(0), 1)
        self.assertEqual(self.n0.get_parent_multiplicity(-1), 1)

    def test_set_parent_multiple_values_node(self):
        """Test the set_parent_ids method given a list with duplicates."""
        self.n0.set_parent_ids([0, 0, 1, 1, 0, 2])
        self.assertIn(0, self.n0.get_parent_ids())
        self.assertIn(1, self.n0.get_parent_ids())
        self.assertIn(2, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(0), 3)
        self.assertEqual(self.n0.get_parent_multiplicity(1), 2)
        self.assertEqual(self.n0.get_parent_multiplicity(2), 1)

    def test_set_children_ids_empty_list_node(self):
        """Test the set_children_ids method given an empty list."""
        self.n0.set_children_ids([])
        self.assertEqual(self.n0.get_children_ids(), [])

    def test_set_children_ids_node(self):
        """Test the set_children_ids method given a valid list."""
        self.n0.set_children_ids([0, 1])
        self.assertIn(0, self.n0.get_children_ids())
        self.assertIn(1, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(0), 1)
        self.assertEqual(self.n0.get_child_multiplicity(1), 1)

    def test_set_child_negative_id_node(self):
        """Test the set_children_ids method given a list with a strictly negative
        ID."""
        self.n0.set_children_ids([0, -1])
        self.assertIn(0, self.n0.get_children_ids())
        self.assertIn(-1, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(0), 1)
        self.assertEqual(self.n0.get_child_multiplicity(-1), 1)

    def test_set_child_multiple_values_node(self):
        """Test the set_children_ids method given a list with duplicates."""
        self.n0.set_children_ids([0, 0, 1, 1, 0, 2])
        self.assertIn(0, self.n0.get_children_ids())
        self.assertIn(1, self.n0.get_children_ids())
        self.assertIn(2, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(0), 3)
        self.assertEqual(self.n0.get_child_multiplicity(1), 2)
        self.assertEqual(self.n0.get_child_multiplicity(2), 1)
        
    def test_add_parent_id_node(self):
        """Test the add_parent_id method."""
        self.n0.add_parent_id(10)
        self.assertIn(10, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(10), 1)

    def test_add_parent_existing_id_node(self):
        """Test the add_parent_id method given an existing parent ID."""
        self.n0.add_parent_id(0)
        self.assertIn(0, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(0), 2)

    def test_add_parent_negative_id_node(self):
        """Test the add_parent_id method given a strictly negative ID."""
        self.n0.add_parent_id(-1)
        self.assertIn(-1, self.n0.get_parent_ids())
        self.assertEqual(self.n0.get_parent_multiplicity(-1), 1)

    def test_add_child_id_unique_id_node(self):
        """Test the add_child_id method."""
        self.n0.add_child_id(10)
        self.assertIn(10, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(10), 1)

    def test_add_child_existing_id_node(self):
        """Test the add_child_id method given an existing child ID."""
        self.n0.add_child_id(2)
        self.assertIn(2, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(2), 2)

    def test_add_child_negative_id_node(self):
        """Test the add_child_id method given a strictly negative ID."""
        self.n0.add_child_id(-1)
        self.assertIn(-1, self.n0.get_children_ids())
        self.assertEqual(self.n0.get_child_multiplicity(-1), 1)

    def test_remove_parent_once_existing_id_node(self):
        """Test the remove_parent_once method given an existing parent ID"""
        self.n0.remove_parent_once(0)
        self.assertEqual(self.n0.get_parent_ids(), [])

    def test_remove_parent_once_existing_id_multiplicity_two_node(self):
        """Test the remove_parent_once method given an existing parent ID
        with multiplicity 2"""
        self.n0.add_parent_id(0)
        self.n0.remove_parent_once(0)
        self.assertEqual(self.n0.get_parent_ids(), [0])

    def test_remove_parent_once_nonexistant_id_node(self):
        """Test the remove_parent_once with an nonexistant ID"""
        self.assertRaises(ValueError, self.n0.remove_parent_once, 1)

    def test_remove_child_once_existing_id_node(self):
        """Test the remove_child_once method given an existing child ID"""
        self.n0.remove_child_once(2)
        self.assertEqual(self.n0.get_children_ids(), [])

    def test_remove_child_once_existing_id_multiplicity_two_node(self):
        """Test the remove_child_once method given an existing child ID
        with multiplicity 2"""
        self.n0.add_child_id(2)
        self.n0.remove_child_once(2)
        self.assertEqual(self.n0.get_children_ids(), [2])

    def test_remove_child_once_nonexistant_id_node(self):
        """Test the remove_child_once with an nonexistant ID"""
        self.assertRaises(ValueError, self.n0.remove_child_once, 1)

    def test_remove_parent_id_existant_id_node(self):
        """Test the remove_parent_id method given an existing parent ID
        with multiplicity 2"""
        self.n0.add_parent_id(0)
        self.n0.remove_parent_id(0)
        self.assertEqual(self.n0.get_parent_ids(), [])

    def test_remove_parent_id_nonexistant_id_node(self):
        """Test the remove_parent_once with an nonexistant ID"""
        self.assertRaises(ValueError, self.n0.remove_parent_id, 1)

    def test_remove_child_id_existant_id_node(self):
        """Test the remove_child_id method given an existing child ID
        with multiplicity 2"""
        self.n0.add_child_id(2)
        self.n0.remove_child_id(2)
        self.assertEqual(self.n0.get_children_ids(), [])

    def test_remove_child_id_nonexistant_id_node(self):
        """Test the remove_child_once with an nonexistant ID"""
        self.assertRaises(ValueError, self.n0.remove_child_id, 1)
