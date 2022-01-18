import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

    def test_init_open_digraph(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {}, {1:1})
        g = open_digraph([0], [1], [n0, n1])
        self.assertEqual(g.inputs, [0])
        self.assertEqual(g.outputs, [1])
        self.assertEqual(g.nodes, {0: n0, 1: n1});

    def test_copy_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertIsNot(n0.copy(), n0)

    def test_copy_open_digraph(self):
        n0 = node(0, 'i', {}, {1:1})
        n1 = node(1, 'i', {}, {1:1})
        g = open_digraph([0], [1], [n0, n1])
        self.assertIsNot(g.copy(), g)

    def test_add_child_node(self):
        n0 = node(10, "i", {}, {1:1})
        
        n0.add_child_id(10)
        self.assertEqual(n0.get_id(), 10)
        
if __name__ == '__main__': # the following code is called only when
    unittest.main()
# precisely this file is run
