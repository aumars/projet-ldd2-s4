from .open_digraph import open_digraph


class bool_circ(open_digraph):
    def __init__(self, inputs, outputs, nodes):
        super().__init__(inputs, outputs, nodes)

        if self.is_cyclic():
            raise ValueError("The graph is cyclic.")

    @classmethod
    def bool_circ(cls, g):
        return cls(g.get_inputs(), g.get_outputs(), g.get_nodes())

    def is_well_formed(self):
        """
        Verifies if the graph is well formed. By definition, a graph is well
        formed if and only if:
        - if the node a copy then 

        Returns
        -------
        bool
            Returns True if all the criteria is fulfilled, return False if at
            least one of them is not.
        """
        if self.is_cyclic():
            return False
        
        for node in self.get_nodes():
            if ((node.get_label() == "" and node.indegree() != 1) or 
                ((node.get_label() == "&" or node.get_label() == "|") and node.outdegree() != 1) or
                (node.get_label() == "~" and node.indegree() != 1 and node.outdegree() != 1)):
                return False
            
        return True
        
