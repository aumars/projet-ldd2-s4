from copy import deepcopy
import os
from random import random, sample
import re
from tkinter import N
from urllib.parse import quote 

from .utils import (random_int_matrix,
                    random_triangular_int_matrix,
                    random_oriented_int_matrix,
                    random_symetric_int_matrix)
from .node import node


class open_digraph:
    def __init__(self, inputs, outputs, nodes):
        """
        An open directed graph.

        Parameters
        ----------
        inputs : int list
            The IDs of the input nodes.
        outputs : int list
            The IDs of the output nodes.
        nodes : node iter
            The nodes of the graph.
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.get_id(): node for node in nodes}
        self.next_id = 0 if self.nodes == {} else max(self.nodes.keys()) + 1

    def __str__(self):
        if len(self.get_id_node_map()) == 0:
            return 'empty'
        else:
            return "{{ {}, {} }}".format(", ".join([str(node) for node in self.nodes.values()]),
                                         ", ".join([str(node) + " -> " + str(self.get_node_by_id(child))
                                                    for node in self.nodes.values()
                                                    for child in node.children.keys()]))

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(self):
        """Create an empty graph."""
        return open_digraph([], [], {})

    def copy(self):
        """
        Copy this graph.

        Returns
        -------
        open_digraph
            The copy of this graph.
        """
        return open_digraph(self.inputs, self.outputs, [deepcopy(node.copy()) for node in self.nodes.values()])

    def get_input_ids(self):
        """
        Get the inputs IDs.

        Returns
        -------
        int list
            The list of the inputs IDs
        """
        return self.inputs

    def get_output_ids(self):
        """
        Get the outputs IDs.

        Returns
        -------
        int list
            The list of the outputs IDs
        """
        return self.outputs

    def get_id_node_map(self):
        """
        Get all nodes.

        Returns
        -------
        int->node dict
            A dictionary containing IDs and their corresponding nodes.
        """
        return self.nodes

    def get_nodes(self):
        """
        Get all nodes.

        Returns
        -------
        int list
            A list containing nodes.
        """
        return list(self.nodes.values())

    def get_node_ids(self):
        """
        Get all IDs of nodes.

        Returns
        -------
        int list
            A list containing the IDs of the nodes.
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, id):
        """
        Get the node with an ID.

        Parameters
        ----------
        id : int
            The id of the node.

        Returns
        -------
        node
            The node with this ID.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of an existing node.
        """
        if id not in self.nodes.keys():
            raise ValueError("A node with the ID {} does not exist."
                           .format(id))
        else:
            return self.nodes[id]

    def get_nodes_by_ids(self, ids):
        """
        Get nodes according to a collection of IDs.

        Parameters
        ----------
        ids : iterable object of int
            The list of node IDs to return.

        Returns
        -------
        list of node
            A list containing nodes corresponding to the IDs.
        """
        return [self.get_node_by_id(id) for id in ids]

    def set_input_ids(self, inputs):
        """
        Set the inputs IDs.

        Parameters
        ----------
        inputs : int list
            The input list. Duplicates are removed.
        """
        self.inputs = list(dict.fromkeys(inputs))

    def set_output_ids(self, outputs):
        """
        Set the outputs IDs.

        Parameters
        ----------
            The input list. Duplicates are removed.
        """
        self.outputs = list(dict.fromkeys(outputs))

    def add_input_id(self, id):
        """
        Add a new input ID.

        [id] must be an existing node with no parent and one child, and does
        not exist as an output node.
        If [id] is already an input node, do nothing.

        Parameters
        ----------
        id : int
            The input ID to add.

        Raises
        ------
        ValueError
            If [id] is not an existing node.
        ValueError
            If [id] has parents.
        ValueError
            If [id] does not exactly one child.
        ValueError
            If [id] is an output node.
        """
        if id not in self.get_node_ids():
            raise ValueError("ID {} does not exist as a node."
                             .format(id))
        elif self.get_node_by_id(id).get_parent_ids() != []:
            raise ValueError("{} has parents and cannot be an input node."
                             .format(self.get_node_by_id(id)))
        elif len(self.get_node_by_id(id).get_children_ids()) != 1:
            raise ValueError("{} has {} children and cannot be an input node."
                             .format(self.get_node_by_id(id), len(self.get_node_by_id(id).get_children_ids())))
        elif id in self.get_output_ids():
            raise ValueError("{} is an output node and cannot be an input node."
                             .format(self.get_node_by_id(id)))
        elif id not in self.get_input_ids():
            self.inputs.append(id)

    def add_output_id(self, id):
        """
        Add a new output ID.

        [id] must be an existing node with one parent and no children, and does
        not exist as an input node.
        If [id] is already an output node, do nothing.

        Parameters
        ----------
        id : int
            The output ID to add.

        Raises
        ------
        ValueError
            If [id] is not an existing node.
        ValueError
            If [id] has children.
        ValueError
            If [id] does not exactly one parent.
        ValueError
            If [id] is an input node.
        """
        if id not in self.get_node_ids():
            raise ValueError("ID {} does not exist as a node."
                             .format(id))
        elif self.get_node_by_id(id).get_children_ids() != []:
            raise ValueError("{} has children and cannot be an output node."
                             .format(self.get_node_by_id(id)))
        elif len(self.get_node_by_id(id).get_parent_ids()) != 1:
            raise ValueError("{} has {} parents and cannot be an output node."
                             .format(self.get_node_by_id(id), len(self.get_node_by_id(id).get_parent_ids())))
        elif id in self.get_input_ids():
            raise ValueError("{} is an input node and cannot be an output node."
                             .format(self.get_node_by_id(id)))
        elif id not in self.get_output_ids():
            self.outputs.append(id)

    def new_id(self):
        """
        Generate a new ID.

        Returns
        -------
        int
            A new ID.
        """
        self.next_id += 1
        return self.next_id - 1

    def add_edge(self, src, tgt):
        """
        Add a new edge between two nodes.

        Parameters
        ----------
        src : int
            The ID of the source node.
        tgt : int
            The ID of the target node.

        Raises
        ------
        ValueError
            If [src] does not exist as a node.
        ValueError
            If [tgt] does not exist as a node.
        ValueError
            If [src] is the ID of an output node.
        ValueError
            If [tgt] is the ID of an input node.
        """
        if src not in self.get_node_ids():
            raise ValueError("{} does not correspond to an existing node."
                             .format(src))
        elif tgt not in self.get_node_ids():
            raise ValueError("{} does not correspond to an existing node."
                             .format(tgt))
        elif src in self.get_output_ids():
            raise ValueError("{} is an output node! We cannot"
                             "add an edge from this node"
                             .format(src))
        elif tgt in self.get_input_ids():
            raise ValueError("{} is an input node! We cannot"
                             "add an edge from this node"
                             .format(src))
        else:
            self.get_node_by_id(src).add_child_id(tgt)
            self.get_node_by_id(tgt).add_parent_id(src)

    def add_node(self, label='', parents=[], children=[]):
        """
        Add a new node in the graph, then links it with its parent and its
        child nodes.

        Parameters
        ----------
        label : str, optional
            The label of the new node.
        parents : int list, optional
            The list of the IDs of parent nodes.
        children : int list, optional
            The list of the IDs of child nodes.

        Returns
        -------
        int
            The ID of the new node.

        Raises
        ------
        ValueError
            If one of the IDs in [parents] or [children] does not correspond to
            an ID.
        ValueError
            If one of the IDs in [parents] correspond to an ID of an
            output node.
        ValueError
            If one of the IDs in [children] correspond to an ID of an
            input node or does not correspond to a node.
        """
        P, C = set(parents), set(children)
        N, O, I = set(self.get_id_node_map()), set(self.get_output_ids()), set(self.get_input_ids())
        if not (P.issubset(N) and C.issubset(N)):
            raise ValueError("The following IDs do not correspond "
                             "to existing nodes : {}."
                             .format(P.union(C) - N))
        elif P.intersection(O) != set():
            raise ValueError("The following nodes are output nodes "
                             "and cannot be parents: {}."
                             .format(P.intersection(O)))
        elif C.intersection(I) != set():
            raise ValueError("The following nodes are input nodes "
                             "and cannot be children: {}."
                             .format(C.intersection(I)))
        else:
            id = self.new_id()
            self.nodes[id] = node(id, label,
                                  {parent: 1 for parent in parents},
                                  {child: 1 for child in children})
            for parent in parents:
                self.nodes[parent].add_child_id(id)
            for child in children:
                self.nodes[child].add_parent_id(id)
            return id

    def remove_edges(self, *args):
        """
        Removes an edge between pairs of nodes. If no edges exist between a
        pair of nodes, no error is returned.

        Parameters
        ----------
        *args : tuple of int * int
            Pairs of nodes with the ID of the source node in first and the ID
            of the target node in second.
        """
        for src, tgt in args:
            try:
                s = self.get_node_by_id(src)
                t = self.get_node_by_id(tgt)
                s.remove_child_once(tgt)
                t.remove_parent_once(src)
            except ValueError:
                continue

    def remove_edge(self, src, tgt):
        """
        Remove an edge between two nodes. This is a special case of
        remove_edges.

        Parameters
        ----------
        src : int
            The ID of the source node.
        target : int
            The ID of the target node.
        """
        self.remove_edges((src, tgt))

    def remove_parallel_edges(self, *args):
        """
        Removes parallel edges between pairs of nodes. If no parallel edges
        exist between a pair of nodes, no error is returned.

        Parameters
        ----------
        *args : tuple of int * int
            Pairs of nodes with the ID of the source node in first and the ID
            of the target node in second.
        """
        for src, tgt in args:
            try:
                s = self.get_node_by_id(src)
                t = self.get_node_by_id(tgt)
            except ValueError:
                continue
            if tgt in s.get_children_ids() and src in t.get_parent_ids():
                s.remove_child_id(tgt)
                t.remove_parent_id(src)
            if src in t.get_children_ids() and tgt in s.get_parent_ids():
                t.remove_child_id(src)
                s.remove_parent_id(tgt)

    def remove_nodes_by_id(self, ids):
        """
        Remove nodes. If an ID in [ids] does not correspond to an ID of an
        existing node, no error is thrown.

        Parameters
        ----------
        ids : int list
            List of IDs of nodes.
        """
        for id in ids:
            try:
                n = self.get_node_by_id(id)
            except ValueError:
                continue
            for parent in n.get_parent_ids():
                self.remove_parallel_edges((id, parent))
            for child in n.get_children_ids():
                self.remove_parallel_edges((id, child))
            self.next_fd = min(id, self.next_id)
            del self.nodes[id]
            try:
                input_index = self.get_input_ids().index(id)
                del self.inputs[input_index]
            except ValueError:
                pass
            try:
                output_index = self.get_output_ids().index(id)
                del self.outputs[output_index]
            except ValueError:
                pass

    def remove_node_by_id(self, id):
        """
        Remove a node. This is a special case of remove_nodes_by_id.

        Parameters
        ----------
        id : int
            The ID of a node.
        """
        self.remove_nodes_by_id([id])

    def is_well_formed(self):
        """
        Verifies if the graph is well formed. By definition, a graph is well
        formed if and only if:
        - each input node and output node exists in the graph
        - each input node has a unique child of multiplicity 1 and no parent
        - each output node has a unique parent of multiplicity 1 and no child
        - each ID (key) in [self.nodes] corresponds to the ID of its node
          (value)
        - if a j as a child i of multplivity m, then i must have a parent j of
          multiplicity m, and vice-versa

        Returns
        -------
        bool
            Returns True if all the criteria is fulfilled, return False if at
            least one of them is not.
        """
        for input in self.get_input_ids():
            if input not in self.get_node_ids():
                return False

            i = self.get_node_by_id(input)
            i_children = i.get_children_ids()

            if not (len(i_children) == 1
                    and i.get_child_multiplicity(i_children[0]) == 1
                    and i.get_parent_ids() == []):
                return False

        for output in self.get_output_ids():
            if output not in self.get_node_ids():
                return False

            o = self.get_node_by_id(output)
            o_parents = o.get_parent_ids()

            if not (len(o_parents) == 1
                    and o.get_parent_multiplicity(o_parents[0]) == 1
                    and o.get_children_ids() == []):
                return False

        for id, noeud in self.get_id_node_map().items():
            if id != noeud.get_id():
                return False
            for child_id in noeud.get_children_ids():
                child = self.get_node_by_id(child_id)
                if noeud.get_child_multiplicity(child_id) != child.get_parent_multiplicity(id):
                    return False

        return True

    def add_input_node(self, id):
        """
        Adds an input node.

        Parameters
        ----------
        id : int
            The ID of the input node's child.
        
        Returns
        -------
        int
            The ID of the new input node.
        
        Raises
        ------
        ValueError
            If [id] does not correspond to an existing node.
        ValueError
            If [id] is the ID of an input node.
        """
        if id not in self.get_node_ids():
            raise ValueError("{} does not correspond to an existing node."
                             .format(id))
        elif id in self.get_input_ids():
            raise ValueError("{} is an input node and thus cannot be the "
                             "child of another input node."
                             .format(self.get_node_by_id(id)))

        elif (id in self.get_output_ids() and
            len(self.get_node_by_id(id).get_parent_ids()) > 0):
            raise ValueError("{} is an output that already has a parent."
                             .format(self.get_node_by_id(id)))
        else:
            new_id = self.add_node(children=[id])
            self.add_input_id(new_id)
            return new_id

    def add_output_node(self, id):
        """
        Adds an output node.

        Parameters
        ----------
        id : int
            The ID of the output node's parent.
        
        Returns
        -------
        int
            The ID of the new output node.

        Raises
        ------
        ValueError
            If [id] does not correspond to an existing node.
        ValueError
            If [id] is the ID of an output node.
        """
        if id not in self.get_node_ids():
            raise ValueError("{} does not correspond to an existing node."
                             .format(id))
        elif id in self.get_output_ids():
            raise ValueError("{} is an output node and thus cannot be the "
                             "parent of another input node."
                             .format(self.get_node_by_id(id)))

        elif (id in self.get_input_ids() and
            len(self.get_node_by_id(id).get_children_ids()) > 0):
            raise ValueError("{} is an input that already has a child."
                             .format(self.get_node_by_id(id)))
        else:
            new_id = self.add_node(parents=[id])
            self.add_output_id(new_id)
            return new_id

    @classmethod
    def graph_from_adjacency_matrix(cls, A):
        """
        Generate graph from adjacency matrix.

        Parameters
        ----------
        A : list list int
            Adjacency matrix

        Returns
        -------
        open_digraph
           Graph
        """
        G = cls.empty()
        n = len(A)
        node_ids = [G.add_node() for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(A[i][j]):
                    G.add_edge(node_ids[i], node_ids[j])
        return G

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free",
               number_generator=random):
        """
        Generate random graph.

        Parameters
        ----------
        n : int
            Length of list
        bound : int
            Upper bound of our random positive integers.
        inputs : int, optional
            Number of input nodes.
        outputs : int, optional
            Number of output nodes.
        form : str, optional
            Type of graph, here are the available options:
            - free : Completely random graph.
            - loop-free : Random graph with no edge between the same node.
            - undirected : Undirected graph
            - loop-free undirected : Undirected graph with no edge between the
                                     same node.
            - oriented : Directed graph with the edges of each pair of nodes
                         pointing only towards one end.
            - DAG : Directed acyclic graph.
        number_generator : callable, optional
            Random number generator that generates real numbers between 0 and 1
            (included or excluded). If [number_generator] generates real
            positive numbers, only the non-integer part is kept.

        Returns
        -------
        open_digraph
           Graph

        Raises
        ------
        ValueError
            If [value] is not recognised as a supported option.
        """
        if inputs > n or outputs > n:
            raise ValueError("More inputs and outputs than available.")
        input_children = sample(range(n), k=inputs)
        output_parents = sample(range(n), k=outputs)
        if form == "free" or form == "loop-free":
            if form == "free":
                A = random_int_matrix(n, bound, null_diag=False,
                                      number_generator=number_generator)
            else:
                A = random_int_matrix(n, bound,
                                      number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        elif form == "undirected" or form == "loop-free undirected":
            if form == "undirected":
                A = random_symetric_int_matrix(n, bound, null_diag=False,
                                               number_generator=number_generator)
            else:
                A = random_symetric_int_matrix(n, bound,
                                               number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
                    A[i][j] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
                    A[j][i] = 0
        elif form == "oriented":
            A = random_oriented_int_matrix(n, bound,
                                           number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        elif form == "DAG":
            A = random_triangular_int_matrix(n, bound,
                                             number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        else:
            return ValueError("{} is not a supported option."
                              .format(form))
        G = cls.graph_from_adjacency_matrix(A)
        for i in input_children:
            G.add_input_node(i)
        for o in output_parents:
            G.add_output_node(o)
        return G

    def node_dict(self):
        """
        Generate dictionary of a graph of n associating each ID of a node to a
        unique integer between 0 and n excluded.

        Returns
        -------
        dict int->int
            Dictionary associating a node ID to a unique integer
        """
        N = self.get_node_ids()
        return dict(zip(N, sample(range(len(N)), k=len(N))))

    def adjacency_matrix(self):
        """
        Generate the adjacency matrix of a graph.

        Returns
        ------
        list list int
           Adjacency matrix
        """
        dict = self.node_dict()
        n = len(dict)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for id in dict:
            i = dict[id]
            node = self.get_node_by_id(id)
            for child in node.get_children_ids():
                j = dict[child]
                A[i][j] = node.get_child_multiplicity(child)
        return A
    
    def to_str_dot_format(self, verbose=False):
        """
        Generate a string of the dot format.
        
        Parameters
        ----------
        verbose : boolean, optional
            Set to True to display the nodes IDs. 

        Returns
        ------
        string
           The string of the graph in dot format.
        """
        digraph = "digraph G {\n"

        for node in self.get_nodes():
            form = ("shape=invhouse, " if node.get_id() in self.get_input_ids() else 
                       "shape=house, " if node.get_id() in self.get_output_ids() else "")
            
            id_str = f"\nid: {node.get_id()}" if verbose else ""

            digraph += f"v{ node.get_id() } [{form}label=\"{ node.get_label() }{ repr(id_str)[1:-1] }\"];\n"
        
        for node in self.get_nodes():  
            for parent in node.get_parent_ids():
                line = f"v{parent} -> v{node.get_id()};\n"
                digraph += line * node.get_parent_multiplicity(parent)
        
        digraph += "}"

        return digraph
                

    def save_as_dot_file(self, path, verbose=False):
        """
        Save the graph as dot file.
        
        Parameters
        ----------
        path:
            The path where the file will be saved. Must be in '.dot' format.

        verbose : boolean, optional
            Set to True to display the nodes IDs. 
        """
        f = open(path, "w")
        f.write(self.to_str_dot_format(verbose))
        f.close()

    @classmethod
    def from_dot_file(self, path):
        """
        Create a graph from dot file.
        
        Parameters
        ----------
        path:
            The path where the dot file is saved.

        Returns
        ------
        open_digraph
           The graph corresponds to the file.        
        """
        with open(path, "r") as file:
            f = file.read()
        f = f.split("{")[1].split("}")[0].replace(" ", "").replace("\n", "").split(";")
        f = [l for l in f if l != ""]

        graph = open_digraph.empty()
        dict_node = {}

        in_dict = lambda label: set(dict_node.keys()) & set(label) != set()
        add_node = lambda label: {"id": graph.add_node(label), "parents":set(), "children": set()}
        get_id_dict = lambda label : add_node(label) if not in_dict(label) else dict_node[str_node]["id"]

        for line in f:
            lbl_re = re.search(r".*label=\"(.*?)\"\]", line)
            lbl_node = lbl_re.group(1) if lbl_re != None else ""

            line = line.strip().split("[")[0]

            n_node = len(line.split("->"))
            l = line.split("->")

            for i in range(n_node):
                str_node = line.split("->")[i]                
                dict_node[str_node] = get_id_dict(lbl_node)

                if not lbl_node in dict_node:
                    add_node(lbl_node)
                
                else:
                    l_parents = [get_id_dict(parent) for parent in l[:i]]
                    l_children = [get_id_dict(child) for child in l[i+1:]]

                    dict_node[str_node]["parents"] = dict_node[str_node]["parents"].union(l_parents)
                    dict_node[str_node]["children"] = dict_node[str_node]["children"].union(l_children)

        for str_node in dict_node:
            graph.get_node_by_id(dict_node[str_node]["id"]).set_parent_ids(dict_node[str_node]["parents"])
            graph.get_node_by_id(dict_node[str_node]["id"]).set_children_ids(dict_node[str_node]["children"])
        
        return graph

    def display(self, verbose=False):
        """
        Display the graph in the following website : dreampuf.github.io/GraphvizOnline.
        
        Parameters
        ----------
        verbose : boolean, optional
            Set to True to display the nodes IDs. 
        """
        digraph = quote(self.to_str_dot_format(verbose))
        url = f'https://dreampuf.github.io/GraphvizOnline/#"{digraph}"'
        os.system(f"firefox {url}")

    def sub_is_cyclic(self, graph):
        if graph.get_node_ids() == []:
            return False
        
        else:
            leaf = []
            for n_id in graph.get_node_ids():
                if graph.get_node_by_id(n_id).get_parent_ids() == []:
                    leaf.append(n_id)
                    break

            if leaf == []:
                return True
            
            else:
                graph.remove_node_by_id(leaf[0])
                return graph.is_cyclic()

    def is_cyclic(self):
        return self.sub_is_cyclic(self.copy())
    
    def min_id(self):
        return min(self.get_node_ids())
    
    def max_id(self):
        return max(self.get_node_ids())
    
    def shift_indices(self, n):
        for node in self.get_nodes():
            node.set_id(node.get_id() + n)
    
    def iparallel(self, g):
        for node in g.get_nodes():
            self.add_node(node.get_label(), node.get_parent_ids(), node.get_children_ids())

            if node.get_id() in g.get_input_ids():
                self.add_input_node(node.get_id())

            if node.get_id() in g.get_output_ids():
                self.add_output_node(node.get_id())
    
    def parallel(self, g):
        graph = open_digraph.empty()
        graph.iparallel(self)
        graph.iparallel(g)
        return graph

    def icompose(self, g):
        if len(self.get_input_ids()) != len(g.get_input_ids()):
            raise ValueError("The number of inputs in the graphs don't coincide.")

        if len(self.get_output_ids()) != len(g.get_output_ids()):
            raise ValueError("The number of output in the graphs don't coincide.")
       
        self.shift_indices(self.max_id())
        self.nodes.update(g.get_id_node_map())
        for i in range(len(self.get_input_ids())):
            o_id = self.get_node_by_id(self.get_output_ids()[i])
            parent_o_id = o_id.get_parent_ids()[0]
            self.remove_node_by_id(o_id)
            self.add_edge(parent_o_id, g.get_input_ids()[i])
        self.set_output_ids(g.get_outputs_ids())
    
    @classmethod
    def identity(cls, n):
        graph = cls.empty()
        
        for _ in range(2 * n):
            graph.add_node()
        
        for i in range(2 * n):
            if i % 2 == 0:
                graph.add_edge(i, i + 1)
        
        graph.set_input_ids([2 * i for i in range(n + 1)])
        graph.set_output_ids([2 * i + 1 for i in range(n + 1)])
        
        return graph

    def compose(self, g):
        graph = open_digraph.identity(len(self.get_output_ids()))
        graph.icompose(self)
        graph.icompose(g)
        return graph

    