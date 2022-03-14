
class op_compositions_mx:
    def iparallel(self, list_graph):
        """
        Add graphs parallel to itself.

        Parameters
        ----------
        list_graph : open_digraph list
            A list containing graphs to add.
        """ 
        for graph in list_graph:
            graph = graph.copy()
            self.shift_indices(graph.max_id() + 1)
            self.set_nodes(self.get_nodes() + graph.get_nodes())
            self.set_input_ids(self.get_input_ids() + graph.get_input_ids())
            self.set_output_ids(self.get_output_ids() + graph.get_output_ids())

    def parallel(self, list_graph):
        """
        Add graphs parallel to itself.

        Parameters
        ----------
        list_graph : open_digraph list
            A list containing graphs to add.
        
        Returns
        ------
        open_digraph
           The graph of the fusion of parallel graphs. 
        """ 
        graph = self.empty()
        graph.iparallel([self] + list_graph)
        return graph
    
    def icompose(self, g):
        """
        Compose graph in sequence.
        The graph g is not modified.

        Parameters
        ----------
        g : open_digraph
           A graph to compose in sequence.
        
        Raises
        ------
        ValueError
            If the number of inputs between the graphs don't coincide.
        ValueError
            If the number of outputs between the graphs don't coincide.

        """ 
        if len(self.get_input_ids()) != len(g.get_input_ids()):
            raise ValueError("The number of inputs in the graphs don't coincide.")

        if len(self.get_output_ids()) != len(g.get_output_ids()):
            raise ValueError("The number of output in the graphs don't coincide.")
        
        self.shift_indices(g.max_id())
        self.nodes.update(g.get_id_node_map())
        
        for i in range(len(self.get_input_ids())):
            o_id = self.get_node_by_id(self.get_output_ids()[i])
            id_parent_o = o_id.get_parent_ids()[0]
            
            self.remove_node_by_id(o_id)
            self.add_edge(id_parent_o, g.get_input_ids()[i])
        
        self.set_output_ids(g.get_output_ids())
    
    def compose(self, g):
        """
        Get the composition of the self graph with the graph g.
        The graphs are not modified.

        Parameters
        ----------
        g : open_digraph
           A graph to compose in sequence.
        
        Returns
        ------
        open_digraph
           The composition of the self graph with g.
        """ 
        graph = self.identity(len(self.get_output_ids()))
        graph.icompose(self.copy())
        graph.icompose(g.copy())
        return graph