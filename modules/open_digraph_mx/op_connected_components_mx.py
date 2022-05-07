import copy


class op_connected_components_mx:
    def get_heritage(self, id):
        """
        Get the IDs list of all nodes having a possible path with the
        given node ID in the graph.

        Parameters
        ----------
        id : int
           The ID of the node we want to have the heritage.

        Returns
        -------
        int list
            The list of IDs of nodes
        """
        dist, _ = self.dijkstra(id)
        return list(dist.keys())

    def assoc_nodes_to_comp(self, nodes):
        """
        Associate each node of a list with its components.

        Parameters
        ----------
        nodes : int list
           The IDs of nodes to associate.

        Returns
        -------
        int -> int
            Keys correspond to node IDs. Values correspond to the ID of
            the component where the node is connected.
        """
        dict_comp = {}
        i = 0
        cur_nodes = copy.copy(nodes)
        while len(cur_nodes) > 0:
            n_id = cur_nodes[0]
            heritage = self.get_heritage(n_id)
            for h_id in heritage:
                dict_comp[h_id] = i
            i += 1
            cur_nodes = list(set(cur_nodes) - set(heritage))
        return dict_comp

    def connected_components(self):
        """
        Get the dict which associte each node with its connected components.

        Returns
        ------
        int * (int -> list)
           The number of connected components and a dict where each node
           are associated with its component.
        """
        dict_comp = self.assoc_nodes_to_comp(self.get_node_ids())

        return len(set(dict_comp.values())), dict_comp
