
class op_compositions_mx:
    def iparallel(self, list_graph):
        """
        Add graphs parallel to itself. This functionality only accepts well-formed graphs.

        Parameters
        ----------
        list_graph : open_digraph list
            A list containing graphs to add.
        """
        for graph in list_graph:
            if len(graph.get_id_node_map()) > 0:
                self.separate_indices(graph)
                self.nodes.update(graph.get_id_node_map())
                self.set_input_ids(self.get_input_ids() + graph.get_input_ids())
                self.set_output_ids(self.get_output_ids() + graph.get_output_ids())
                self.next_id = max(self.nodes.keys()) + 1

    @classmethod
    def parallel(cls, list_graph):
        """
        Add graphs parallel to itself. This functionality only accepts well-formed graphs.

        Parameters
        ----------
        list_graph : open_digraph list
            A list containing graphs to add.

        Returns
        ------
        open_digraph
           The graph of the fusion of parallel graphs.
        """
        graph = cls.empty()
        graph.iparallel(list_graph)
        return graph

    def icompose(self, g):
        """
        Compose graph in sequence. The graph g is not modified. This functionality only accepts well-formed graphs.

        Parameters
        ----------
        g : open_digraph
           A graph to compose in sequence.

        Raises
        ------
        ValueError
            If the number of outputs in self do not coincide with the number of inputs in g.
        """
        if len(self.get_output_ids()) != len(g.get_input_ids()):
            raise ValueError("The number of outputs in self do not coincide with the number of inputs in g.")
        elif len(self.get_output_ids()) == 0 and len(g.get_input_ids()) == 0:
            self.iparallel([g])
        elif len(self.get_id_node_map()) == 0 and len(g.get_id_node_map()) > 0:
            self.nodes = g.get_id_node_map()
            self.set_input_ids(g.get_input_ids())
            self.set_output_ids(g.get_output_ids())
        elif len(g.get_id_node_map()) > 0:
            self.separate_indices(g)
            self.nodes.update(g.get_id_node_map())
            for outid, inid in zip(self.get_output_ids(), g.get_input_ids()):
                onode = self.get_node_by_id(outid)
                onode_parent_id = onode.get_parent_ids()[0] # since output node only has 1 parent
                self.add_edge(onode_parent_id, inid)
            self.remove_nodes_by_id(self.get_output_ids())
            self.set_output_ids(g.get_output_ids())
        self.next_id = (max (self.nodes.keys()) if self.nodes.keys() else 0) + 1

    def compose(self, g):
        """
        Get the composition of the self graph with the graph g. The graphs are not modified. This functionality only accepts well-formed graphs.

        Parameters
        ----------
        g : open_digraph
           A graph to compose in sequence.
        
        Returns
        ------
        open_digraph
           The composition of the self graph with g.
        """ 
        graph = self.copy()
        graph.icompose(g)
        return graph
