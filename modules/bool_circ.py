from .open_digraph import open_digraph


class bool_circ(open_digraph):
    """
    A boolean circuit. Inherits from open_digraph class.

    Parameters
    ----------
    inputs : int list
        The IDs of the input nodes.
    outputs : int list
        The IDs of the output nodes.
    nodes : node iter
        The nodes of the graph.

    Raises
    ------
    ValueError
        If the boolean circuit is cyclic.
    """

    def __init__(self, inputs, outputs, nodes):
        super().__init__(inputs, outputs, nodes)

        if self.is_cyclic():
            raise ValueError("The boolean circuit is cyclic.")

    @classmethod
    def bool_circ(cls, g):
        """
        Create a boolean circuit.

        Parameters
        ----------
        g : open_digraph
            A graph.

        Returns
        -------
        bool_circ
            The boolean circuit.
        """
        return cls(g.get_inputs(), g.get_outputs(), g.get_nodes())

    def is_well_formed(self):
        """
        Verifies if the graph is well formed. By definition, a graph is well
        formed if and only if:
        - graph is acyclic.
        - each '' node must have a parent.
        - each '&' and '|' node must have a child.
        - each '~' node must have one parent and one child.

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
