class op_getter_mx:
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
