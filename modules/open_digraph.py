from copy import deepcopy
from random import sample

from modules.open_digraph_mx.op_algorithm_mx import op_algorithm_mx
from modules.open_digraph_mx.op_connected_components_mx import op_connected_components_mx
from modules.open_digraph_mx.op_getter_mx import op_getter_mx
from modules.open_digraph_mx.op_matrix_mx import op_matrix_mx
from modules.open_digraph_mx.op_modify_mx import op_modify_mx
from modules.open_digraph_mx.op_setter_mx import op_setter_mx
from modules.open_digraph_mx.op_special_graph_mx import op_special_graph_mx
from modules.open_digraph_mx.op_tools_mx import op_tools_mx
from .open_digraph_mx.op_compositions_mx import op_compositions_mx
from .open_digraph_mx.op_display_mx import op_display_mx


class open_digraph(op_compositions_mx, 
                   op_connected_components_mx,
                   op_display_mx, 
                   op_getter_mx,
                   op_matrix_mx,
                   op_modify_mx,
                   op_setter_mx,
                   op_special_graph_mx,
                   op_tools_mx,
                   op_algorithm_mx
                   ):
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

    def min_id(self):
        """
        Get the min ID of nodes.

        Returns
        ------
        int
           The ID minimum. If the graph is empty returns 0.
        """
        return min(self.get_node_ids()) if self.get_node_ids() else 0
    
    def max_id(self):
        """
        Get the max ID of nodes.

        Returns
        ------
        int
           The ID maximum. If the graph is empty returns 0.
        """
        return max(self.get_node_ids()) if self.get_node_ids() else 0

    def copy(self):
        """
        Copy this graph.

        Returns
        -------
        open_digraph
            The copy of this graph.
        """
        return open_digraph(self.inputs, self.outputs, [deepcopy(node.copy()) for node in self.nodes.values()])

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
           
    def sub_is_cyclic(self, graph):
        """
        Sub-function to test if a graph is cyclic.

        Parameters
        ----------
        graph : open_digraph
            A graph.

        Returns
        ------
        bool
           True if the graph is cyclic. Otherwise, return False.
        """
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
        """
        Test if a graph is cyclic.

        Returns
        ------
        bool
           True if the graph is cyclic. Otherwise, return False.
        """
        return self.sub_is_cyclic(self.copy())
    
    def shift_indices(self, n):
        """
        Shift the ID of all nodes.

        Parameters
        ----------
        n : int
            The offset value. 
        """        
        shift_list = lambda l :list(map(lambda x : x + n, l))

        for node in self.get_nodes():
            node.set_id(node.get_id() + n)

            for pid in node.parents:
                node.parents[pid] += n
            for cid in node.children:
                node.children[cid] += n

        self.set_nodes(self.get_nodes())
        self.set_input_ids(shift_list(self.get_input_ids()))
        self.set_output_ids(shift_list(self.get_output_ids()))
