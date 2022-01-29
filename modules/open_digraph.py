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
        self.next_id = max(self.nodes.keys()) + 1

    def __str__(self):
        return """Noeuds : {}
Arrêts : {}""".format(", ".join([node for node in self.nodes.values()]),
                      ", ".join([node + " -> " + self.get.node_by_id(child)
                                 for node in self.nodes.values()
                                 for child in node.children.keys()]))

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(self):
        """Create an empty graph."""
        self.inputs = []
        self.outputs = []
        self.nodes = {}
        self.next_id = 0

    def copy(self):
        """
        Copy this graph.

        Returns
        -------
        open_digraph
            The copy of this graph.
        """
        return open_digraph(self.inputs, self.outputs, self.nodes.values())

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
        Add a new input ID. If the ID already exists as an input node,
        do nothing.

        Parameters
        ----------
        id : int
            The input ID to add.

        Raises
        ------
        ValueError
            If [id] already exists as a output node or an internal node.
        """
        if id in self.get_output_ids() or (id in self.get_node_ids() and id
                                           not in self.get_input_ids()):
            raise ValueError("ID {} already exists as a output node "
                             "or an internal node."
                             .format(id))
        elif id not in self.inputs:
            self.inputs.append(id)

    def add_output_id(self, id):
        """
        Add a new output ID. If the ID already exists as an output node,
        do nothing.

        Parameters
        ----------
        id : int
            The output ID to add.

        Raises
        ------
        ValueError
            If [id] already exists as a input node or an internal node.
        """
        if id in self.get_input_ids() or (id in self.get_node_ids() and id
                                          not in self.get_output_ids()):
            raise ValueError("ID {} already exists as a input node "
                             "or an internal node."
                             .format(id))
        elif id not in self.outputs:
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
        S = set(parents).union(set(children)) - set(self.get_node_ids())
        if S != set():
            raise ValueError("The following IDs do not correspond "
                             "to existing nodes : {}."
                             .format(S))
        O = set(parents) & set(self.get_output_ids())
        if O != set():
            raise ValueError("The following nodes are output nodes "
                             "and cannot be parents: {}."
                             .format(O))

        I = set(children) & set(self.get_input_ids())
        if I != set():
            raise ValueError("The following nodes are input nodes "
                             "and cannot be children: {}."
                             .format(I))

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
            self.inputs.append(new_id)
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
            self.outputs.append(new_id)
            return new_id
