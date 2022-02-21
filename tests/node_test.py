from modules.node import node
import unittest
import sys
import os
from hypothesis import given, strategies as st
from collections import Counter
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


class NodeTest(unittest.TestCase):
    """Tests of the node class."""

    @given(id=st.integers(),
           label=st.text(),
           parents=st.dictionaries(st.integers(), st.integers(min_value=0)),
           children=st.dictionaries(st.integers(), st.integers(min_value=0)))
    def test_valid_init_node(self, id, label, parents, children):
        """Test the constructor with valid parameters."""
        n = node(id, label, parents, children)
        self.assertIsInstance(n, node)

    @given(id=st.integers(),
           label=st.text(),
           parents=st.dictionaries(st.integers(), st.integers(max_value=-1), min_size=1),
           children=st.dictionaries(st.integers(), st.integers(max_value=-1), min_size=1))
    def test_invalid_init_node(self, id, label, parents, children):
        """Test the constructor with invalid parameters."""
        self.assertRaises(ValueError, node, id, label, parents, children)

    @given(node_strategy())
    def test_copy_node(self, n):
        """Test the copy method."""
        self.assertIsNot(n.copy(), n)

    @given(node_strategy())
    def test_get_id_node(self, n):
        """Test the get_id method."""
        self.assertEqual(n.get_id(), n.id)

    @given(node_strategy())
    def test_get_label_node(self, n):
        """Test the get_label method."""
        self.assertEqual(n.get_label(), n.label)

    @given(node_strategy())
    def test_get_parent_ids_node(self, n):
        """Test the get_parents_ids method."""
        self.assertEqual(n.get_parent_ids(), list(n.parents.keys()))

    @given(node_strategy())
    def test_get_children_ids_node(self, n):
        """Test the get_children_ids method."""
        self.assertEqual(n.get_children_ids(), list(n.children.keys()))

    @given(node_strategy(), st.integers())
    def test_get_parent_multiplicity_node(self, n, parent_id):
        """Test the get_parent_multiplicity method."""
        self.assertEqual(n.get_parent_multiplicity(parent_id), n.parents.get(parent_id, 0))

    @given(node_strategy(), st.integers())
    def test_get_child_multiplicity_nonexistant_id_node(self, n, child_id):
        """Test the get_child_multiplicity method."""
        self.assertEqual(n.get_parent_multiplicity(child_id), n.parents.get(child_id, 0))

    @given(node_strategy(), st.integers())
    def test_set_id_node(self, n, id):
        """Test the set_id method."""
        n.set_id(id)
        self.assertEqual(n.get_id(), id)

    @given(node_strategy(), st.text())
    def test_set_label_node(self, n, label):
        """Test the set_label method."""
        n.set_label(label)
        self.assertEqual(n.get_label(), label)

    @given(node_strategy(), st.lists(st.integers()))
    def test_set_parent_ids_node(self, n, parents):
        """Test the set_parent_ids method."""
        parents_count = Counter(parents)
        n.set_parent_ids(parents)
        self.assertCountEqual(n.get_parent_ids(), list(set(parents)))
        for key, value in parents_count.items():
            self.assertEqual(n.get_parent_multiplicity(key), value)

    @given(node_strategy(), st.lists(st.integers()))
    def test_set_children_ids_node(self, n, children):
        """Test the set_children_ids method."""
        children_count = Counter(children)
        n.set_children_ids(children)
        self.assertCountEqual(n.get_children_ids(), list(set(children)))
        for key, value in children_count.items():
            self.assertEqual(n.get_child_multiplicity(key), value)

    @given(node_strategy(), st.integers())
    def test_add_parent_id_node(self, n, parent_id):
        """Test the add_parent_id method."""
        m = n.get_parent_multiplicity(parent_id)
        n.add_parent_id(parent_id)
        self.assertEqual(n.get_parent_multiplicity(parent_id), m + 1)

    @given(node_strategy(), st.integers())
    def test_add_child_id_node(self, n, child_id):
        """Test the add_child_id method."""
        m = n.get_child_multiplicity(child_id)
        n.add_child_id(child_id)
        self.assertEqual(n.get_child_multiplicity(child_id), m + 1)

    @given(node_strategy(), st.integers())
    def test_remove_parent_once_node(self, n, parent_id):
        """Test the remove_parent_once method."""
        m = n.get_parent_multiplicity(parent_id)
        n.remove_parent_once(parent_id)
        if m > 0:
            m = m - 1
        self.assertEqual(n.get_parent_multiplicity(parent_id), m)

    @given(node_strategy(), st.integers())
    def test_remove_child_once_node(self, n, child_id):
        """Test the remove_child_once method."""
        m = n.get_child_multiplicity(child_id)
        n.remove_child_once(child_id)
        if m > 0:
            m = m - 1
        self.assertEqual(n.get_child_multiplicity(child_id), m)

    @given(node_strategy(), st.integers())
    def test_remove_parent_id_node(self, n, parent_id):
        """Test the remove_parent_id method."""
        n.remove_parent_id(parent_id)
        self.assertNotIn(parent_id, n.get_parent_ids())

    @given(node_strategy(), st.integers())
    def test_remove_child_id_node(self, n, child_id):
        """Test the remove_child_id method."""
        n.remove_child_id(child_id)
        self.assertNotIn(child_id, n.get_children_ids())

    @given(node_strategy())
    def test_indegree_node(self, n):
        self.assertEqual(n.indegree(), sum(n.parents.values()))

    @given(node_strategy())
    def test_outdegree_node(self, n):
        self.assertEqual(n.outdegree(), sum(n.children.values()))

    @given(node_strategy())
    def test_degree_node(self, n):
        self.assertEqual(n.degree(), sum(n.parents.values()) + sum(n.children.values()))
