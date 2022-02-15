import open_digraph

class bool_circ(open_digraph):
    def __init__(self, g):
        super().__init__(g.get_input(), g.get_output(), g.get_nodes().keys())
        self.g = g
        
        if self.is_cyclic():
            raise ValueError("The graph is cyclic.")
        

    def sub_is_cyclic(self, nodes):
        if len(nodes) == 0:
            return False
        
        else:
            if nodes == []:
                return True
            
            else:
                return self.is_cyclic(nodes.pop())

    def is_cyclic(self):
        return self.sub_is_cyclic(self.g.get_nodes().copy())
    
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

        for node in self.g.get_nodes():
            if ((node.get_label() == "" and node.indegree() != 1) or 
                ((node.get_label() == "&" or node.get_label() == "|") and node.outdegree() != 1) or
                (node.get_label() == "~" and node.indegree() != 1 and node.outdegree() != 1)):
                return False
        
        return True
