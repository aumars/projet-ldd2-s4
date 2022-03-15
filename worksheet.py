from modules.open_digraph import *
from modules.node import node


# i0 = node(10, "i0", {}, {0: 1})
# i1 = node(11, "i1", {}, {2: 1})

n0 = node(0, "0", {}, {3: 1})
n1 = node(1, "1", {}, {5: 1, 8: 1, 4: 1})
n2 = node(2, "2", {}, {4: 1})

n3 = node(3, "3", {0: 1}, {5: 1, 6: 1, 7: 1})
n4 = node(4, "4", {1: 1, 2: 1}, {6: 1})

n5 = node(5, "5", {3: 1, 1: 1}, {7: 1})
n6 = node(6, "6", {3: 1, 4: 1}, {8:1, 9:1})

n7 = node(7, "7", {5: 1, 3: 1}, {})
n8 = node(8, "8", {1: 1, 6: 1}, {})
n9 = node(9, "9", {6: 1}, {})

# o0 = node(12, "o0", {7: 1}, {})

G = open_digraph([], [], [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9])

# print(G.is_well_formed())
print(G.topological_sort())

# G2.display(True)

# print(G2.is_well_formed())
# print(G.connected_components())
# print(G2.connected_components())
# G2.connected_components()
