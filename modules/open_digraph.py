class node:
    def __init__(self, identity, label, parents, children):
        """
        A graph node.

        Parameters
        ----------
        identity : int
            Its unique ID in the graph. The ID must be a positive integer.
        label : str
            A string.
        parents : int->int dict
            Maps a parent node's id to its multiplicity
        children : int->int dict
            Maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        return "N({})".format(self.id)

    def __repr__(self):
        return str(self)

    def copy(self):
        """
        Copy the node.

        Returns
        -------
        node
            The copy of this node.
        """
        return node(self.id, self.label, self.parents, self.children)

    def get_id(self):
        """
        Get the ID.

        Returns
        -------
        int
            The node ID.
        """
        return self.id

    def get_label(self):
        """
        Get the label.

        Returns
        -------
        string
            The node label.
        """
        return self.label

    def get_parent_ids(self):
        """
        Get the IDs of all the parents.

        Returns
        -------
        list of int
            A list containing the IDs of all parents.
        """
        return list(self.parents.keys())

    def get_parent_multiplicity(self, id):
        """
        Get the multiplicity of a parent

        Parameters
        ----------
        id : int
            The ID of the parent node.

        Returns
        -------
        int
            The multiplicity of the parent node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a parent node.
        """
        if id not in self.get_parent_ids():
            raise ValueError("{} does not have a parent with the ID {}"
                             ".".format(self, id))
        else:
            return self.parents[id]

    def get_children_ids(self):
        """
        Get the IDs of all the children.

        Returns
        -------
        list of int
            A list containing the IDs of all children.
        """
        return list(self.children.keys())

    def get_child_multiplicity(self, id):
        """
        Get the multiplicity of a child

        Parameters
        ----------
        id : int
            The ID of the child node.

        Returns
        -------
        int
            The multiplicity of the child node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a child node.
        """
        if id not in self.get_children_ids():
            raise ValueError("{} does not have a child with the ID {}"
                             ".".format(self, id))
        else:
            return self.children[id]

    def set_id(self, id):
        """
        Set the node ID.

        Parameters
        ----------
        id : int
            The node ID.
        """
        self.id = id

    def set_label(self, label):
        """
        Set the node label.

        Parameters
        ----------
        label : str
            The node label.
        """
        self.label = label

    def set_parent_ids(self, parents_ids):
        """
        Set the parents of the node.

        Parameters
        ----------
        parents_ids : int->int dict
            A dictionary containing the parents of the node.
        """
        self.parents.clear()
        for parent in parents_ids:
            self.parents[parent] = 1

    def set_children_ids(self, children_ids):
        """
        Set the children of the node.

        Parameters
        ----------
        children_ids : int->int dict
            A dictionary containing the children of the node.
        """
        self.children.clear()
        for child in children_ids:
            self.children[child] = 1

    def add_child_id(self, child):
        """
        Add a new child to the node.

        Parameters
        ----------
        child : int
            The ID of the child node.
        """
        if child not in self.children.keys():
            self.children[child] = 1
        else:
            self.children[child] += 1

    def add_parent_id(self, parent):
        """
        Add a new parent to the node.

        Parameters
        ----------
        parent : int
            The ID of the parent node.
        """
        if parent not in self.parents.keys():
            self.parents[parent] = 1
        else:
            self.parents[parent] += 1

    def remove_parent_once(self, id):
        """
        Remove one occurence of a parent node.

        Parameters
        ----------
        id : int
            The ID of the parent node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a parent node.
        """
        if id not in self.get_parent_ids():
            raise ValueError("{} does not have a parent with the ID {}"
                             ".".format(self, id))
        else:
            if self.parents[id] == 1:
                del self.parents[id]
            else:
                self.parents[id] -= 1

    def remove_child_once(self, id):
        """
        Remove one occurence of a child node.

        Parameters
        ----------
        id : int
            The ID of the child node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a child node.
        """
        if id not in self.get_children_ids():
            raise ValueError("{} does not have a child with the ID {}"
                             ".".format(self, id))
        else:
            if self.children[id] == 1:
                del self.children[id]
            else:
                self.children[id] -= 1

    def remove_child_id(self, id):
        """
        Remove all occurences of a child node.

        Parameters
        ----------
        id : int
            The ID of the child node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a child node.
        """
        if id not in self.get_children_ids():
            raise ValueError("{} does not have a child with the ID {}"
                             ".".format(self, id))
        else:
            del self.children[id]

    def remove_parent_id(self, id):
        """
        Remove all occurences of a parent node.

        Parameters
        ----------
        id : int
            The ID of the parent node.

        Raises
        ------
        ValueError
            If [id] is not recognised as the ID of a parent node.
        """
        if id not in self.get_parents_ids():
            raise ValueError("{} does not have a parent with the ID {}"
                             ".".format(self, id))
        else:
            del self.parents[id]


class open_digraph:
    def __init__(self, inputs, outputs, nodes):
        """
        An open directed graph.

        Parameters
        ----------
        inputs : list of int
            The IDs of the input nodes.
        outputs : list of int
            The IDs of the output nodes.
        nodes : iterable object
            The nodes of the graph.
        """
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}
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
        list of int
            The list of the inputs IDs
        """
        return self.inputs

    def get_output_ids(self):
        """
        Get the outputs IDs.

        Returns
        -------
        list of int
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
        list of int
            A list containing nodes.
        """
        return list(self.nodes.values())

    def get_node_ids(self):
        """
        Get all IDs of nodes.

        Returns
        -------
        list of int
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
        KeyError
            If [id] is not recognised as the ID of an existing node.
        """
        if id not in self.nodes.keys():
            raise KeyError("A node with the ID {} does not exist.".format(id))
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
        return [self.get_node_by_id(id) for id in ids

    def set_input_ids(self, inputs):
        """
        Set the inputs IDs.

        Parameters
        ----------
        inputs : list of int
            The input list.
        """
        self.inputs = inputs

    def set_output_ids(self, outputs):
        """
        Set the outputs IDs.

        Parameters
        ----------
        outputs : list of int
            The outputs list.
        """
        self.outputs = outputs

    def add_input_id(self, id):
        """
        Add a new input ID.

        Parameters
        ----------
        id : int
            The input ID to add.
        """
        if id not in self.inputs:
            self.inputs.append(id)

    def add_output_id(self, id):
        """
        Add a new output ID.

        Parameters
        ----------
        id : int
            The output ID to add.
        """
        if id not in self.outputs:
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
            If [src] is the ID of an output node.
        ValueError
            If [tgt] is the ID of an input node.
        """
        if src in self.get_output_ids():
            raise ValueError("{} is an output node! We cannot"
                             "add an edge from this node".format(src))
        if tgt in self.get_input_ids():
            raise ValueError("{} is an input node! We cannot"
                             "add an edge from this node".format(src))
        self.nodes[src].add_child_id(tgt)
        self.nodes[tgt].add_parent_id(src)

    def add_node(self, label='', parents=[], children=[]):
        """
        Add a new node in the graph, then links it with its parent and its
        child nodes.

        Parameters
        ----------
        label : str, optional
            The label of the new node.
        parents : list of int, optional
            The list of the IDs of parent nodes.
        children : list of int, optional
            The list of the IDs of child nodes.

        Returns
        -------
        int
            The ID of the new node.

        Raises
        ------
        ValueError
            If one of the IDs in [parents] correspond to an ID of an
            output node.
        ValueError
            If one of the IDs in [children] correspond to an ID of an
            input node.
        """
        O = set(parents) & set(self.get_output_ids())
        if O != set():
            raise ValueError("The following nodes are output nodes"
                             "and cannot be parents: {}".format(O))

        I = set(children) & set(self.get_input_ids())
        if I != set():
            raise ValueError("The following nodes are input nodes"
                             "and cannot be children: {}".format(I))

        id = self.new_id()
        self.nodes[id] = node(id, label, parents, children)
        for parent in parents:
            self.nodes[parent].add_child_id(id)
        for child in children:
            self.nodes[child].add_parent_id(id)

        return id

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

    def remove_edges(self, *args):
        """
        Removes edges between pairs of nodes.

        Parameters
        ----------
        *args : tuple of int * int
            Pairs of nodes with the ID of the source node in first and the ID
            of the target node in second.

        Raises
        ------
        ValueError
            If the ID of a target node does not exist as the ID of a child of
            its source node.
        ValueError
            If the ID of a source node does not exist as the ID of a parent of
            its child node.
        """
        for src, tgt in args:
            s = self.get_node_by_id(src)
            t = self.get_node_by_id(tgt)
            if tgt not in s.get_children_ids():
                raise ValueError("ID {} does not exist as a"
                                 "child of source node {}".format(tgt, s))
            elif src not in t.get_parent_ids():
                raise ValueError("ID {} does not exist as a"
                                 "parent of target node {}".format(src, t))
        for src, tgt in args:
            s = self.get_node_by_id(src)
            t = self.get_node_by_id(tgt)
            s.remove_child_id(tgt)
            t.remove_parent_id(src)

    def remove_parallel_edges(self, *args):
        """
        Removes parallel edges between pairs of nodes.

        Parameters
        ----------
        *args : tuple of int * int
            Pairs of nodes with the ID of the source node in first and the ID
            of the target node in second.

        Raises
        ------
        ValueError
            If no parallel edges exist between a pair of nodes.
        """
        for src, tgt in args:
            s = self.get_node_by_id(src)
            t = self.get_node_by_id(tgt)
            if not ((tgt in s.get_children_ids()
                     and src in t.get_parent_ids())
                    or (src in t.get_children_ids()
                     and tgt in s.get_parent_ids())):
                raise ValueError("Parallel edges do not exist between"
                                 "{} and {}".format(s, t))
        for src, tgt in args:
            s = self.get_node_by_id(src)
            t = self.get_node_by_id(tgt)
            if tgt in s.get_children_ids() and src in t.get_parent_ids():
                s.remove_child_id(tgt)
                t.remove_parent_id(src)
            if src in t.get_children_ids() and tgt in s.get_parent_ids():
                t.remove_child_id(src)
                s.remove_parent_id(tgt)

    def remove_node_by_id(self, id):
        """
        Remove a node. This is a special case of remove_nodes_by_id.

        Parameters
        ----------
        id : int
            The ID of a node.
        """
        self.remove_nodes_by_id([id])

    def remove_nodes_by_id(self, ids):
        """
        Remove nodes.

        Parameters
        ----------
        ids : list of int
            List of IDs of nodes.

        Raises
        ------
        ValueError
            If an ID in [ids] does not correspond to an ID of an existing node.
        """
        S =  set(self.get_node_ids()) - set(ids)
        if S != set():
            raise ValueError("The following IDs do not correspond to"
                             "existing nodes: {}.".format(S))
        else:
            for id in ids:
                n = self.get_node_by_id(id)
                for parent in n.get_parent_ids():
                    self.remove_parallel_edges((id, parent))
                for child in n.get_children_ids():
                    self.remove_parallel_edges((id, child))
                self.next_fd = min(id, self.next_id)
                del self.nodes[id]

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

        for output in self.get_ouput_by_ids():
            if output not in self.get_node_ids():
                return False

            o = self.get_node_by_id(output)
            o_parents = i.get_parents_ids()

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

        Raises
        ------
        ValueError
            If [id] is the ID of an input node.
        """
        if id is in self.get_input_ids():
            raise ValueError("{} is an input node and thus cannot be the "
                             "child of another input "
                             "node.".format(self.get_node_by_id(id)))
        new_id = self.add_node(children=[id])
        self.add_input_id(new_id)

    def add_output_node(self, id)
        """
        Adds an output node.

        Parameters
        ----------
        id : int
            The ID of the output node's parent.

        Raises
        ------
        ValueError
            If [id] is the ID of an output node.
        """
        if id is in self.get_output_ids():
            raise ValueError("{} is an output node and thus cannot be the "
                             "parent of another input "
                             "node.".format(self.get_node_by_id(id)))
        new_id = self.add_node(parents=[id])
        self.add_output_id(new_id)
