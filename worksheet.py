from modules.open_digraph import *
n0 = node(0, 'a', {3: 1, 4: 1}, {1: 1, 2: 1})
n1 = node(1, 'b', {0: 1}, {2: 2, 5: 1})
n2 = node(2, 'c', {0: 1, 1: 2}, {6: 1})

i0 = node(3, 'i0', {}, {0: 1})
i1 = node(4, 'i1', {}, {0: 1})

o0 = node(5, 'o0', {1: 1}, {})
o1 = node(6, 'o1', {2: 1}, {})

G = open_digraph([3, 4], [5, 6], [n0, n1, n2,
                                  i0, i1,
                                  o0, o1])


i0 = node(0, "i0", {}, {6: 1})
i1 = node(1, "i1", {}, {4: 1})
i2 = node(2, "i2", {}, {4: 1})
i3 = node(3, "i3", {}, {9: 1})

n0 = node(4, "a", {1: 1, 2: 1, 15: 1}, {5: 1})
n1 = node(5, "b", {4: 1}, {7: 1, 8: 1, 14: 1})
n2 = node(6, "g", {0: 1}, {7: 1})
n3 = node(7, "c", {5: 1, 6: 1}, {11: 1})
n4 = node(8, "f", {5: 1}, {12: 1})
n5 = node(9, "d", {3: 1}, {10: 1})
n6 = node(10, "e", {9: 1}, {13: 1})
n7 = node(14, "h", {5: 1}, {})
n8 = node(15, "k", {}, {4: 1})

o0 = node(11, "o0", {7: 1}, {})
o1 = node(12, "o1", {8: 1}, {})
o2 = node(13, "o2", {10: 1}, {})

G2 = open_digraph([0, 1, 2, 3], [11, 12, 13], [i0, i1, i2, i3,
                                               n0, n1, n2, n3, n4, n5, n6, n7, n8,
                                               o0, o1, o2])


# G2.display(True)

# print(G2.is_well_formed())
print(G.connected_components())
print(G2.connected_components())
# G2.connected_components()
