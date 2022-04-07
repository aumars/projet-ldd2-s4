from random import choice
from .open_digraph import open_digraph


class bool_circ(open_digraph):
    """
    A boolean circuit. Inherits from open_digraph class.
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
                # We create a node at '(' which begins a variable.
                if char == '(':
                    node = g.get_node_by_id(current_node)
                    if len(node.get_label()) == 0 and len(s2) > 0 and s2[0] != 'x':
                        node.set_label(s2)
                    pid = g.add_node()
                    g.add_edge(pid, current_node)
                    if len(s2) > 0 and s2[0] == 'x':
                        if s2 not in labels:
                            labels[s2] = [current_node]
                        else:
                            if current_node not in labels[s2]:
                                labels[s2].append(current_node)
                    current_node = pid
                    s2 = ''
                # We set the current_node at ')' which ends a variable.
                elif char == ')':
                    node = g.get_node_by_id(current_node)
                    if len(node.get_label()) == 0 and len(s2) > 0 and s2[0] != 'x':
                        node.set_label(s2)
                    if len(s2) > 0 and s2[0] == 'x':
                        if s2 not in labels:
                            labels[s2] = [current_node]
                        else:
                            if current_node not in labels[s2]:
                                labels[s2].append(current_node)
                    current_node = node.get_children_ids()[0]
                    s2 = ''
                else:
                    s2 += char
        for s2 in labels:
            for i in range(1, len(labels[s2])):
                g.merge_nodes_by_id(labels[s2][0], labels[s2][i])
        for s2 in list(sorted(labels)):
            g.add_input_node(labels[s2][0])
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
            if node.get_id() not in self.get_input_ids() and node.get_id() not in self.get_output_ids():
                label = node.get_label()

                COND_COPY = label == "" and node.indegree() != 1 
                COND_AND_OR = (label == "&" or label == "|") and node.outdegree() != 1 
                COND_NOT = label == "~" and (node.indegree() != 1 or node.outdegree() != 1)
                COND_ILLEGAL = label in ILLEGAL
            
                if COND_ILLEGAL or COND_COPY or COND_AND_OR or COND_NOT:
                    return False

        return True

    @classmethod
    def from_binary(cls, bit_string):
        """
        Construct a boolean circuit from given binary numbers.

        Parameters
        ----------
        bit_string : string
            A bit string of the truth table output.

        Returns
        -------
        bool_circ
            The boolean circuit representing the bit string.

        Raises
        ------
        ValueError
            If the length of the argument bit_string is not a power of 2.
        ValueError
            If bit_string is not composed of bit.
        """
        not_pow2 = f"bit_string = {bit_string} is not a power of 2."
        if len(bit_string) == 0:
            raise ValueError("Empty bit_string.")
        for c in bit_string:
            if c != '0' and c != '1':
                raise ValueError(f"bit_string = {bit_string} is not entirely composed of bits.")
        if bin(len(bit_string))[2] == '0':
            raise ValueError(not_pow2)
        for c in bin(len(bit_string))[3:]:
            if c == '1':
                raise ValueError(not_pow2)
        g = cls.from_open_digraph(open_digraph.empty())
        n = len(bin(len(bit_string))) - 3
        oid = g.add_node('|')
        g.add_output_node(oid)
        vars = {}
        for i in range(n):
            pid = g.add_node()
            iid = g.add_input_node(pid)
            g.variables["x" + str(i)] = iid
            vars[i] = pid
        for i, k in enumerate(bit_string):
            if k == '1':
                a = g.add_node('&')
                g.add_edge(a, oid)
                for j in bin(int(k))[3:]:
                    if j == '0':
                        g.add_edge(vars[i % n], a)
                    else:
                        id = g.add_node('~')
                        g.add_edge(vars[i % n], id)
                        g.add_edge(id, a)
        return g

    @classmethod
    def random(cls, n):
        """
        Generate a random bool_circ graph.

        Parameters
        ----------
        n : int
            The number of input and output in the graph. This number must be greater than 0.

        Returns
        -------
        bool_circ
            A random bool_circ graph.
        """
        UNAIRE = ['', '~']
        BINAIRE = ['&', '|', '^']
        if n <= 0:
            raise ValueError(f"n = {n} doit être strictement positif.")
        g = open_digraph.random(n, 1, inputs=n, outputs=n, form="DAG")
        for id, n in g.get_id_node_map().items():
            if n.indegree() == 1 and n.outdegree() == 1:
                n.set_label(choice(UNAIRE))
            elif n.indegree() > 1 and n.outdegree() == 0:
                n.set_label(choice(BINAIRE))
            elif n.indegree() > 1 and n.outdegree() > 1:
                uop = n
                ucp_id = g.add_node()
                g.get_node_by_id(ucp_id).children = uop.children
                uop.children = {}
                g.add_edge(uop.get_id(), ucp_id)
        return g

    @classmethod
    def adder(cls, n):
    """

    Parameters
    ----------
    n: int
        Puissance de 2

    Returns
    -------

    Raises
    ------
    ValueError
        If the length of the argument r1 or r2 is not a power of 2.
    """
    g = bool_circ(open_digraph.empty())
    if n == 0:
        x0 = g.add_node()
        x1 = g.add_node()
        x2 = g.add_node()
        g.add_input_node(x0)
        g.add_input_node(x1)
        g.add_input_node(x2)
        xor1 = g.add_node()
        g.add_edge(x0, xor1)
        g.add_edge(x1, xor1)
        copie1 = g.add_node()
        g.add_edge(xor1, copie1)
        and1 = g.add_node()
        and2 = g.add_node()
        xor2 = g.add_node()
        g.add_edge(x0, and1)
        g.add_edge(x1, and1)
        g.add_edge(copie1, and2)
        g.add_edge(x2, and2)
        g.add_edge(copie1, xor1)
        g.add_edge(x2, xor1)
        or1 = g.add_node()
        g.add_edge(and1, or1)
        g.add_edge(and2, or1)
        g.add_output_node(or1)
        g.add_output_node(xor1)
    else:
        adder1 = cls.adder(n - 1)
        adder2 = cls.adder(n - 1)

        adder1variables = list(sorted(adder1.variables.items()))
        adder2variables = list(sorted(adder2.variables.items()))

        adder1varA = adder1variables[:n/2]
        adder1varB = adder1variables[n/2:]

        adder2varA = adder2variables[:n/2]
        adder2varB = adder2variables[n/2:]

        return parallel(adder1, adder2)


def half_adder(self, n):
    """
    """ 
    pass
