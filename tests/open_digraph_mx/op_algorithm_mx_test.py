from tests.strategy import random_well_formed_open_digraph_strategy
from modules.node import node
from modules.open_digraph import open_digraph
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_algorithm_mx_test(unittest.TestCase):
    def setUp(self):
        n0 = node(0, '0', {10: 1}, {3: 1})
        n1 = node(1, '1', {}, {4: 1, 5: 1, 8: 1})
        n2 = node(2, '2', {11: 1}, {4: 1})
        n3 = node(3, '3', {0: 1}, {5: 1, 6: 1, 7: 1})
        n4 = node(4, '4', {1: 1, 2: 1}, {6: 1})
        n5 = node(5, '5', {1: 1, 3: 1}, {7: 1})
        n6 = node(6, '6', {3: 1, 4: 1}, {8: 1, 9: 1})
        n7 = node(7, '7', {3: 1, 5: 1}, {12: 1})
        n8 = node(8, '8', {1: 1, 6: 1}, {})
        n9 = node(9, '9', {6: 1}, {})

        i0 = node(10, 'I0', {}, {0: 1})
        i1 = node(11, 'I1', {}, {2: 1})
        o0 = node(12, 'O0', {7: 1}, {})
        self.graph = open_digraph([10, 11], [12], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, i0, i1, o0])

    @given(random_well_formed_open_digraph_strategy(), st.integers(), st.one_of(st.integers(), st.just(None)), st.sampled_from([None, -1, 1]))
    def test_dijkstra(self, graph, src, tgt, direction):
        """
        On vérifie que :
        - dist contient uniquement les IDs des noeuds, comme valeurs une distance valide (entre 0 et N inclus)
        - prev contient uniquement les IDs des noeuds, comme valeurs une ID qui est son parent

        On ne vérifie pas que :
        - la distance est correcte
        - la longueur de dist et de prev est valide
        - tgt, si spécifié, est dans dist et prev
        """
        if src in graph.get_node_ids() and (tgt is None or tgt in graph.get_node_ids()):
            dist, prev = graph.dijkstra(src, tgt, direction)
            N = len(graph.get_node_ids())
            for k, v in dist.items():
                self.assertIn(k, graph.get_node_ids())
                self.assertGreaterEqual(v, 0)
                self.assertLessEqual(v, N)
            for k, v in prev.items():
                self.assertIn(k, graph.get_node_ids())
        else:
            self.assertRaises(ValueError, graph.dijkstra, src, tgt, direction)

    @given(random_well_formed_open_digraph_strategy(), st.integers(), st.integers())
    def test_shortest_path(self, graph, src, tgt):
        """
        On vérifie que :
        - les IDs sont correctes.
        - les IDs forment un chemin

        On ne vérifie pas que :
        - le chemin est le plus court possible
        """
        if src in graph.get_node_ids() and tgt in graph.get_node_ids():
            try:
                chemin = graph.shortest_path(src, tgt)
            except RuntimeError:
                pass
            for srcid, tgtid in zip(chemin[:-1], chemin[1:]):
                srcnode, tgtnode = graph.get_node_by_id(srcid), graph.get_node_by_id(tgtid)
                self.assertIn(srcid, tgtnode.get_parent_ids())
                self.assertIn(tgtid, srcnode.get_children_ids())
        else:
            self.assertRaises(ValueError, graph.shortest_path, src, tgt)

    @given(random_well_formed_open_digraph_strategy(), st.integers(), st.integers())
    def test_common_ancestry(self, graph, foo, bar):
        """
        On vérifie que :
        - les IDs des noeuds sont bons
        - les dist des ancêtres communs sont bons (on utilise dijkstra)
        """
        if foo in graph.get_node_ids() and bar in graph.get_node_ids():
            ancestry = graph.common_ancestry(foo, bar)
            #  N = len(graph.get_node_ids())
            for k, v in ancestry.items():
                self.assertIn(k, graph.get_node_ids())
                self.assertEqual(len(v), 2)
                # self.assertGreaterEqual(v[0], 0)
                # self.assertGreaterEqual(v[1], 0)
                # self.assertLessEqual(v[0], N)
                # self.assertLessEqual(v[1], N)

                distfoo, _ = graph.dijkstra(foo, k)
                distbar, _ = graph.dijkstra(bar, k)

                self.assertEqual(distfoo[k], v[0])
                self.assertEqual(distbar[k], v[1])
        else:
            self.assertRaises(ValueError, graph.common_ancestry, foo, bar)

    def test_common_ancestry_example(self):
        ancestry = self.graph.common_ancestry(5, 8)
        self.assertCountEqual(ancestry.keys(), [0, 3, 1])
        self.assertEqual(ancestry[0], (2, 3))
        self.assertEqual(ancestry[3], (1, 2))
        self.assertEqual(ancestry[1], (1, 1))

    @given(random_well_formed_open_digraph_strategy(form='DAG'))
    def test_topological_sort(self, graph):
        """
        Only tested for directed acyclic graphs. Cyclic graphs lead to an infinite loop and thus cannot be tested.
        We check if the descendants of a node in a level is in a level below, and if that node has at least one child at the level directly below
        """
        toposort = graph.topological_sort()
        for i, level in enumerate(toposort):
            for id in level:
                node = graph.get_node_by_id(id)
                node_children = node.get_children_ids()

                def find_descendants(node, lvl, toposort):
                    for descendants in enumerate(toposort, lvl + 1):
                        if node in descendants:
                            return True
                    return False

                def find_direct_descendant(node, lvl):
                    for child in node.get_children_ids():
                        if child in lvl:
                            return True
                    return False

                if i != len(toposort) - 1:
                    self.assertTrue(find_direct_descendant(node, toposort[i + 1]))
                    for child in node_children:
                        self.assertTrue(find_descendants(child, i, toposort))

    def test_topological_sort_example(self):
        topology = self.graph.topological_sort()
        self.assertCountEqual(topology[0], [0, 1, 2])
        self.assertCountEqual(topology[1], [3, 4])
        self.assertCountEqual(topology[2], [5, 6])
        self.assertCountEqual(topology[3], [7, 8, 9])

    @given(random_well_formed_open_digraph_strategy(), st.integers())
    def test_node_depth(self, graph, node):
        if node in graph.get_node_ids() and not graph.is_cyclic():
            depth = graph.node_depth(node)
            toposort = graph.topological_sort()
            self.assertIn(node, toposort[depth])
        else:
            self.assertRaises(ValueError, graph.node_depth, node)

    @given(random_well_formed_open_digraph_strategy())
    def test_depth(self, graph):
        if not graph.is_cyclic():
            self.assertEqual(graph.depth(), len(graph.topological_sort()))
        else:
            self.assertRaises(ValueError, graph.depth)

    @given(random_well_formed_open_digraph_strategy(), st.integers(), st.integers())
    def test_longest_path(self, graph, src, tgt):
        """
        We check:
        - the chemin has valid nodes
        - the distance is correct

        We do not check:
        - if the distance is the longest possible
        """
        if src in graph.get_node_ids() and tgt in graph.get_node_ids() and not graph.is_cyclic():
            chemin, dist = graph.longest_path(src, tgt)
            self.assertEqual(len(chemin), dist)
            for srcid, tgtid in zip(chemin[:-1], chemin[1:]):
                srcnode, tgtnode = graph.get_node_by_id(srcid), graph.get_node_by_id(tgtid)
                self.assertIn(srcid, tgtnode.get_parent_ids())
                self.assertIn(tgtid, srcnode.get_children_ids())
        else:
            self.assertRaises(ValueError, graph.longest_path, src, tgt)

    def test_longest_path_example(self):
        _, dist = self.graph.longest_path(1, 5)
        self.assertEqual(dist, 1)
