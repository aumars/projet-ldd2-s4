from modules.node import node
from modules.open_digraph import open_digraph
from hypothesis import strategies as st
from hypothesis import assume
import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)


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


@st.composite
def open_digraph_strategy(draw):
    nodes = draw(st.lists(node_strategy()))
    io_num = draw(st.integers(min_value=0, max_value=len(nodes)))
    input_num = draw(st.integers(min_value=0, max_value=io_num))
    io_ids = draw(st.permutations([node.get_id() for node in nodes]).map(lambda x: x[:io_num]))
    input_ids = io_ids[:input_num]
    output_ids = io_ids[input_num+1:]
    return open_digraph(input_ids, output_ids, nodes)


@st.composite
def random_well_formed_open_digraph_strategy(draw, inputs=True, outputs=True, form=None):
    if form is None:
        form = draw(st.sampled_from(['free', 'loop-free', 'undirected', 'loop-free undirected', 'oriented', 'DAG']))
    n = draw(st.integers(min_value=0, max_value=20))
    bound = draw(st.integers(min_value=0, max_value=10))
    if inputs:
        inputs = draw(st.integers(min_value=0, max_value=n/2))
    else:
        inputs = 0
    if outputs:
        outputs = draw(st.integers(min_value=0, max_value=n/2))
    else:
        outputs = 0
    graph = open_digraph.random(n, bound, inputs, outputs, form)
    assume(graph.is_well_formed())
    return graph
