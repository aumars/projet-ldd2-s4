from tests.strategy import random_well_formed_open_digraph_strategy
import unittest
import sys
import os
from hypothesis import given, strategies as st
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)  # allows us to fetch files from the project root


class op_algorithm_mx_test(unittest.TestCase):
    @given(random_well_formed_open_digraph_strategy, st.integers(), st.one_of(st.integers(), st.just(None)), st.sampled_from([None, -1, 1]))
    def test_dijkstra(self, graph, src, tgt, direction):
        """
        On vérifie que :
        - dist contient uniquement les IDs des noeuds, comme valeurs une distance valide (entre 0 et N inclus)
        - prev contient uniquement les IDs des noeuds, comme valeurs une ID qui est son parent
        - la longueur de dist et de prev est valide
        - tgt, si spécifié, est dans dist et prev

        On ne vérifie pas que :
        - la distance est correcte
        """
        if src in graph.get_node_ids() and (tgt is None or tgt in graph.get_node_ids()):
            dist, prev = graph.dijkstra(src, tgt, direction)
            N = len(graph.get_node_ids())
            # Peut-être -1 ?
            # self.assertEqual(len(prev), N)
            for k, v in dist.items():
                self.assertIn(k, graph.get_node_ids())
                self.assertGreaterEqual(v, 0)
                self.assertLessEqual(v, N)
            for k, v in prev.items():
                self.assertIn(k, graph.get_node_ids())
                # si k=src ?
                # self.assertIn(v, graph.get_node_ids())
                # self.assertIn(v, graph.get_node_by_id(k).get_parent_ids(k))
            if tgt is None:
                self.assertEqual(len(dist), N)
                self.assertEqual(len(prev), N)
            else:
                self.assertIn(tgt, dist.keys())
                self.assertIn(tgt, prev.keys())
        else:
            self.assertRaises(ValueError, graph.dijkstra, src, tgt, direction)

    @given(random_well_formed_open_digraph_strategy, st.integers(), st.integers())
    def test_shortest_path(self, graph, src, tgt):
        """
        On vérifie que :
        - les IDs sont correctes.
        - les IDs forment un chemin

        On ne vérifie pas que :
        - le chemin est le plus court possible
        """
        if src in graph.get_node_ids() and tgt in graph.get_node_ids():
            chemin = graph.shortest_path(src, tgt)
            for srcid, tgtid in zip(chemin[:-1], chemin[1:]):
                srcnode, tgtnode = graph.get_node_by_id(srcid), graph.get_node_by_id(tgtid)
                self.assertIn(srcid, tgtnode.get_parent_ids())
                self.assertIn(tgtid, srcnode.get_children_ids())
        else:
            self.assertRaises(ValueError, graph.shortest_path, src, tgt)

    @given(random_well_formed_open_digraph_strategy, st.integers(), st.integers())
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

    @given(random_well_formed_open_digraph_strategy())
    def test_topological_sort(self, graph):
        """
        We check if the descendants of a node in a level is in a level below, and if that node has at least one child at the level directly below
        """
        if not graph.is_cyclic():
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

                    if i != len(toposort) - 1:
                        self.assertNotEqual(set(node_children).intersection(set(toposort[i+1])), set())
                        for child in node_children:
                            self.assertTrue(find_descendants(child, i, toposort))
        else:
            self.assertRaises(ValueError, graph.topological_sort)

    @given(random_well_formed_open_digraph_strategy(), st.integers())
    def test_node_depth(self, graph, node):
        if node in graph.get_node_ids() and not graph.is_cyclic():
            depth = graph.node_dept(node)
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
