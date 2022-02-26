from modules.node import node

class op_modify_mx:
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
