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
        Construct a binary circuit from a propositional formula.

        The index of the circuit's [inputs] attribute correspond to the
        index of the variable in the propositional formula, thus x0
        will correspond to index 0 of [inputs], x1 will correspond to
        index 1, etc.
        If a variable in the propositional formula is missing, for
        example, if x0 is omitted, then the indices are shifted
        leftward accordingly, so x1 will correspond to index 0...

        Parameters
        ----------
        *args
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

        LEGAL = ['0',
                 '1',
                 '',   # Copie
                 '~',  # NOT
                 '&',  # AND
                 '|',  # OR
                 '^'   # OU EXCLUSIF
                 ]
        for node in self.get_nodes():
            if node.get_id() not in self.get_input_ids() and node.get_id() not in self.get_output_ids():
                label = node.get_label()

                COND_COPY = label == '' and node.indegree() != 1
                COND_AND_OR = (label == '&' or label == '|' or label == '^') and node.outdegree() != 1
                COND_NOT = label == '~' and (node.indegree() != 1 or node.outdegree() != 1)
                COND_ILLEGAL = label not in LEGAL
            
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
            g.add_input_node(pid)
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
        Construct an adder circuit for n-bit registers.

        Parameters
        ----------
        n: int
            Number of bits for the registers that the adder circuit
            is designed for.

        Returns
        -------
        bool_circ
            An adder circuit.

        Raises
        ------
        ValueError
            If [n] is not positive.
        """
        if n < 0:
            raise ValueError(f"n = {n} must be positive.")
        if n == 0:
            g = cls.from_open_digraph(open_digraph.empty())
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
            g.add_output_node(xor2)
            return g
        else:
            adder1 = cls.adder(n - 1)
            adder2 = cls.adder(n - 1)

            adder1.separate_indices(adder2)
            adder1.nodes.update(adder2.get_id_node_map())
            adder1.set_output_ids(adder1.get_output_ids()
                                  + adder2.get_output_ids())[1:]
            adder1.add_edge(adder2.outputs[0],
                            adder1.inputs[len(adder1.inputs)])
            adder1.set_input_ids(adder1.get_input_ids()[:n//2]
                                 + adder2.get_input_ids()[:n//2]
                                 + adder1.get_input_ids()[n//2:n-1]
                                 + adder2.get_input_ids()[n//2:])
            return adder1

    @classmethod
    def half_adder(cls, n):
        """
        Construct an half-adder circuit for n-bit registers.

        Parameters
        ----------
        n: int
            Number of bits for the registers that the adder circuit
            is designed for.

        Returns
        -------
        bool_circ
            An half-adder circuit.

        Raises
        ------
        ValueError
            If [n] is not positive.
        """
        g = cls.adder(n)
        g.get_node_by_id(g.get_input_ids()[-1]).set_label('0')
        g.set_input_ids(g.get_input_ids()[:-1])
        return g

    @classmethod
    def register(cls, n, value):
        """
        Construct a boolean circuit that represents an instanciated
        register of a given integer.

        Parameters
        ----------
        n: int
            Size of register.

        value: int
            Value of register.

        Returns
        -------
        bool_circ
            Instanciated register of an integer.

        Raises
        ------
        ValueError
            If [n] is not positive.
        ValueError
            If [value] is not positive.
        ValueError
            If [value] cannot be represented in binary with [n] bits.
        """
        if n < 0:
            raise ValueError(f"n = {n} is not positive.")
        if value < 0:
            raise ValueError(f"value = {value} is not positive.")
        if 2 ** n - 1 < value:
            raise ValueError(f"value = {value} cannot be represented"
                             "with n = {n} bits.")
        binary = bin(value)[2:]
        binary = "0" * (n - len(binary)) + binary
        g = cls.from_open_digraph(open_digraph.empty())
        for k in binary:
            id = g.add_node()
            g.add_output_node(id)
            ip = g.add_input_node(id)
            g.get_node_by_id(ip).set_label(k)
        return g

    def trans_copy(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                children = node.get_children_ids()
                if label == '0' or label == '1':
                    for child_id in children:
                        child = self.get_node_by_id(child_id)
                        for child_copie_id in child.get_children_ids():
                            new_id = self.add_node(label=label)
                            self.add_edge(new_id, child_copie_id)
                        self.remove_node_by_id(child)
                    self.remove_node_by_id(id)

    def trans_not(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                children = node.get_children_ids()
                for child_id in children:
                    child = self.get_node_by_id(child_id)
                    if label == '0':
                        child.set_label('1')
                    else:
                        child.set_label('0')
                self.remove_node_by_id(id)

    def trans_and(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                if label == '0':
                    children = node.get_children_ids()
                    for child_id in children:
                        child = self.get_node_by_id(child_id)
                        for p in child.get_parent_ids():
                            if p != id:
                                self.remove_parallel_edges((p, child_id))
                                new_id = self.add_node()
                                self.add_edge(p, new_id)
                        child.set_label(label)
                self.remove_node_by_id(id)

    def trans_or(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                if label == '1':
                    children = node.get_children_ids()
                    for child_id in children:
                        child = self.get_node_by_id(child_id)
                        for p in child.get_parents():
                            if p != id:
                                self.remove_parallel_edges(p, child_id)
                                new_id = self.add_node()
                                self.add_edge(p, new_id)
                        child.set_label(label)
                self.remove_node_by_id(id)

    def trans_xor(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                if label == '1':
                    children = node.get_children_ids()
                    for child_id in children:
                        child = self.get_node_by_id(child_id)
                        for c in child.get_children_ids():
                            new_id = self.add_node('~')
                            self.add_edge(child_id, new_id)
                            self.add_edge(new_id, c)
                        if len(child.get_children_ids()) == 0:
                            new_id = self.add_node('~')
                            self.add_edge(child_id, new_id)
                self.remove_node_by_id(id)

    def trans_neutral(self, ids):
        for id in ids:
            node = self.get_node_by_id(id)
            if len(node.get_parent_ids()) == 0:
                label = node.get_label()
                if label == '|' or label == '^':
                    node.set_label('0')
                elif label == '&':
                    node.set_label('1')

    def transform(self, ids):
        """
        Apply a simplifying transformation to a list of concerned nodes.
        These nodes must have no parents.

        Parameters
        ----------
        ids: list of int
            List of valid node IDs.
        """
        self.trans_copy(ids)
        self.trans_not(ids)
        self.trans_and(ids)
        self.trans_or(ids)
        self.trans_xor(ids)
        self.trans_neutral(ids)

    def evaluate(self):
        """
        Evaluate the boolean circuit.

        Returns
        -------
        str
            Calculated result of the boolean circuit.
        """
        def get_no_parents(self):
            ids = []
            for node in self.get_nodes():
                if len(node.get_parents()) == 0:
                    ids.append(node.get_id())
            return ids

        def result(self):
            for out_id in self.get_output_ids():
                out = self.get_node_by_id(out_id)
                if len(out.get_parent_ids()) != 1:
                    return False
            return True

        g = self.copy()

        while not g.result():
            g.transform(g.get_no_parents())

        bit_string = ""
        for out_id in g.get_output_ids():
            out = g.get_node_by_id(out_id)
            node = g.get_node_by_id(out.get_parents()[0])
            bit_string.append(node.get_label())
        return bit_string
