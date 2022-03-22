from .open_digraph import open_digraph


class bool_circ(open_digraph):
    """
    A boolean circuit. Inherits from open_digraph class.

    Attributes
    ----------
    variables: str -> int dict
        Map associating variables to their corresponding input node IDs.
    """

    def __init__(self, inputs, outputs, nodes):
        """
        Construct a boolean circuit from given nodes. The nodes must not form a cycle.

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
        super().__init__(inputs, outputs, nodes)

        if self.is_cyclic():
            raise ValueError("The boolean circuit is cyclic.")

        self.variables = {}

    @classmethod
    def from_open_digraph(cls, g):
        """
        Create a boolean circuit from an open directed graph.

        Parameters
        ----------
        g : open_digraph
            A graph.

        Returns
        -------
        bool_circ
            The boolean circuit.
        """
        return cls(g.get_input_ids(), g.get_output_ids(), g.get_id_node_map())

    @classmethod
    def from_formula(cls, *args):
        """
        Construct a tree from a propositional formula.

        Parameters
        ----------
        *args : str
            Propositional formulas

        Returns
        -------
        g : bool_circ
            A tree constructed from [s].
        """
        g = cls.from_open_digraph(open_digraph.empty())
        labels = {}
        for s in args:
            id = g.add_node()
            g.add_output_node(id)
            current_node = id
            s2 = ''
            for char in s:
                if char == '(':
                    node = g.get_node_by_id(current_node)
                    node.set_label(s2)
                    pid = g.add_node()
                    g.add_edge(pid, current_node)
                    if s2 in labels:
                        g.merge_nodes_by_id(current_node, labels[s2])
                    elif s2[0] == 'x':
                        labels[s2] = node
                        current_node = pid
                    s2 = ''
                elif char == ')':
                    node = g.get_node_by_id(current_node)
                    node.set_label(s2)
                    if s2 in labels:
                        g.merge_nodes_by_id(current_node, labels[s2])
                    elif s2[0] == 'x':
                        labels[s2] = node
                        current_node = g.node.get_children_ids()[0]
                    s2 = ''
                else:
                    s2 += char
        for s2 in labels:
            g.variables[s2] = g.add_input_node(labels[s2].get_node_id())
        return g

    def is_well_formed(self):
        """
        Verifies if the graph is well formed. By definition, a graph is well
        formed if and only if:
        - graph is acyclic.
        - each '' node must have a parent.
        - each '&' and '|' node must have a child.
        - each '~' node must have one parent and one child.
        - each label is different to 'COPIE', 'NOT', 'AND' and 'OR'.

        Returns
        -------
        bool
            Returns True if all the criteria is fulfilled, return False if at
            least one of them is not.
        """
        if self.is_cyclic():
            return False

        ILLEGAL = ["COPIE", "NOT", "AND", "OR"]

        for node in self.get_nodes():
            label = node.get_label()
            
            COND_COPY = label == "" and node.indegree() != 1 
            COND_AND_OR = (label == "&" or label == "|") and node.outdegree() != 1 
            COND_NOT = label == "~" and (node.indegree() != 1 or node.outdegree() != 1)
            COND_ILLEGAL = label in ILLEGAL
            
            if COND_ILLEGAL or COND_COPY or COND_AND_OR or COND_NOT:
                return False

        return True
