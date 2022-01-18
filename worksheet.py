from modules.open_digraph import *
import inspect
n0 = node(0, "0", {}, {1: 1})
n1 = node(1, "1", {0: 1}, {2: 1})
n2 = node(2, "2", {1: 1}, {3: 1})
n3 = node(3, "3", {3: 1}, {})
g = open_digraph([0], [3], [n0, n1, n2, n3])
print(inspect.getsource(open_digraph))
print(inspect.getdoc(open_digraph))
print(inspect.getsourcefile(open_digraph))
