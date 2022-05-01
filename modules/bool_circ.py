from random import choice
from .open_digraph import open_digraph


class bool_circ(open_digraph):
    """
    A boolean circuit. Inherits from open_digraph class.
    """

    def __init__(self, inputs, outputs, nodes, not_cyclic=False):
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
        not_cyclic : bool, optional
            If the given graph is not already cyclic.

        Raises
        ------
        ValueError
            If the boolean circuit is cyclic.
        """
        super().__init__(inputs, outputs, nodes)

        if not not_cyclic and self.is_cyclic():
            raise ValueError("The boolean circuit is cyclic.")

    @classmethod
    def from_open_digraph(cls, g, not_cyclic=False):
        """
        Create a boolean circuit from an open directed graph.

        Parameters
        ----------
        g : open_digraph
            A graph.
        not_cyclic : bool, optional
            If the given graph is not already cyclic.

        Returns
        -------
        bool_circ
            The boolean circuit.
        """
        return cls(g.get_input_ids(), g.get_output_ids(), g.get_nodes(), not_cyclic)

    @classmethod
    def empty(cls):
        """
        Construct an empty binary circuit.
        """
        return cls.from_open_digraph(super().empty())

    def copy(self):
        """
        Construct a copy of the current binary circuit.
        """
        return bool_circ.from_open_digraph(super().copy(), not_cyclic=True)

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
            g = cls.empty()
            x0 = g.add_node('')
            x1 = g.add_node('')
            x2 = g.add_node('')
            g.add_input_node(x0)
            g.add_input_node(x1)
            g.add_input_node(x2)
            xor1 = g.add_node('^')
            g.add_edge(x0, xor1)
            g.add_edge(x1, xor1)
            copie1 = g.add_node('')
            g.add_edge(xor1, copie1)
            and1 = g.add_node('&')
            and2 = g.add_node('&')
            xor2 = g.add_node('^')
            g.add_edge(x0, and1)
            g.add_edge(x1, and1)
            g.add_edge(copie1, and2)
            g.add_edge(x2, and2)
            g.add_edge(copie1, xor2)
            g.add_edge(x2, xor2)
            or1 = g.add_node('|')
            g.add_edge(and1, or1)
            g.add_edge(and2, or1)
            g.add_output_node(or1)
            g.add_output_node(xor2)
            return g
        else:
            adder = cls.parallel([cls.adder(n - 1), cls.adder(n - 1)])
            adder_inputs = adder.get_input_ids()
            adder_outputs = adder.get_output_ids()

            k = 2 ** (n - 1)
            adder1_a = adder_inputs[:k]
            adder1_b = adder_inputs[k:2*k]
            adder1_c = adder_inputs[2*k]
            adder1_cprime = adder_outputs[0]
            adder1_r = adder_outputs[1:2*k]

            adder2_a = adder_inputs[2*k+1:3*k+1]
            adder2_b = adder_inputs[3*k+1:4*k+1]
            adder2_c = adder_inputs[4*k+1]
            adder2_cprime = adder_outputs[2*k]
            adder2_r = adder_outputs[2*k+1:]

            adder.set_output_ids([adder1_c] + adder1_r + adder2_r)
            adder.set_input_ids(adder1_a + adder2_a
                                + adder1_b + adder2_b + [adder2_c])
            adder.add_edge(adder2_cprime, adder1_c)
            return adder

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
        inputs = g.get_input_ids()
        g.get_node_by_id(inputs[-1]).set_label('0')
        g.set_input_ids(inputs[:-1])
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

    def _trans_copy_one(self, id):
        def trans_copy_one_child(self, child, label):
            for child_copie_id in child.get_children_ids():
                new_id = self.add_node(label=label)
                self.add_edge(new_id, child_copie_id)
            self.remove_node_by_id(child.get_id())

        node = self.get_node_by_id(id)
        if len(node.get_parent_ids()) == 0:
            label = node.get_label()
            children = node.get_children_ids()
            if label == '0' or label == '1':
                remove = False
                for child_id in children:
                    child = self.get_node_by_id(child_id)
                    if child.get_label() == '':
                        trans_copy_one_child(self, child, label)
                        remove = True
                if remove:
                    self.remove_node_by_id(id)

    def trans_copy(self, ids):
        for id in ids:
            self._trans_copy_one(id)

    def _trans_not_one(self, id):
        if id not in self.get_node_ids():
            return
        node = self.get_node_by_id(id)
        if len(node.get_parent_ids()) == 0:
            label = node.get_label()
            children = node.get_children_ids()
            if label == '0' or label == '1':
                remove = False
                for child_id in children:
                    child = self.get_node_by_id(child_id)
                    child_label = child.get_label()
                    if child_label == '~':
                        if child_label == '0':
                            child.set_label('1')
                        else:
                            child.set_label('0')
                        remove = True
                if remove:
                    self.remove_node_by_id(id)

    def trans_not(self, ids):
        for id in ids:
            self._trans_not_one(id)

    def _trans_andor_one(self, id, p, q, op):
        if id not in self.get_node_ids():
            return
        node = self.get_node_by_id(id)
        if len(node.get_parent_ids()) == 0:
            label = node.get_label()
            if label == p:
                children = node.get_children_ids()
                for child_id in children:
                    child = self.get_node_by_id(child_id)
                    child_label = child.get_label()
                    if child_label == op:
                        for p in child.get_parent_ids():
                            if p != id:
                                self.remove_parallel_edges((p, child_id))
                                new_id = self.add_node()
                                self.add_edge(p, new_id)
                    child.set_label(label)
            if label == p or label == q:
                self.remove_node_by_id(id)

    def _trans_and_one(self, id):
        self._trans_andor_one(id, '0', '1', '&')

    def _trans_or_one(self, id):
        self._trans_andor_one(id, '1', '0', '|')

    def trans_and(self, ids):
        for id in ids:
            self._trans_and_one(id)

    def trans_or(self, ids):
        for id in ids:
            self._trans_or_one(id)

    def _trans_xor_one(self, id):
        if id not in self.get_node_ids():
            return
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
            if label == '1' or label == '0':
                self.remove_node_by_id(id)

    def trans_xor(self, ids):
        for id in ids:
            self._trans_xor_one(id)

    def _trans_neutral_one(self, id):
        if id not in self.get_node_ids():
            return
        node = self.get_node_by_id(id)
        label = node.get_label()
        if label == '|' or label == '^':
            node.set_label('0')
        elif label == '&':
            node.set_label('1')

    def trans_neutral(self, ids):
        for id in ids:
            self._trans_neutral_one(id)

    def transform(self, ids):
        """
        Apply a simplifying transformation to a list of concerned nodes.
        These nodes must have no parents.

        Parameters
        ----------
        ids: list of int
            List of valid node IDs.
        """
        for id in ids:
            self._trans_copy_one(id)
            self._trans_not_one(id)
            self._trans_and_one(id)
            self._trans_or_one(id)
            self._trans_xor_one(id)
            self._trans_neutral_one(id)
            # print([node.get_id() for nodex in self.get_nodes() if len(node.get_parent_ids()) == 0 and len(node.get_children_ids()) == 0])
        self.remove_nodes_by_id([node.get_id() for node in self.get_nodes() if len(node.get_parent_ids()) == 0 and len(node.get_children_ids()) == 0])

    def get_no_parents(self):
        ids = []
        for node in self.get_nodes():
            if len(node.get_parent_ids()) == 0 and node.get_id() not in self.get_output_ids() and len(node.get_children_ids()) == 1 and node.get_children_ids()[0] not in self.get_output_ids():
                ids.append(node.get_id())
        return ids

    def transform_all(self):
        self.transform(self.get_no_parents())

    def transform_full(self):
        while len(self.get_output_ids()) * 2 != len(self.get_id_node_map()):
            self.transform_all()

    def evaluate(self):
        """
        Evaluate the boolean circuit.

        Returns
        -------
        str
            Calculated result of the boolean circuit.
        """
        g = self.copy()
        g.transform_full()

        bit_string = ""
        for out_id in g.get_output_ids():
            out = g.get_node_by_id(out_id)
            node = g.get_node_by_id(out.get_parent_ids()[0])
            bit_string += node.get_label()
        return bit_string

    @classmethod
    def encoder(cls):
        graph = bool_circ.empty()
        i0 = graph.add_node()
        i1 = graph.add_node()
        i2 = graph.add_node()
        i3 = graph.add_node()

        o0 = graph.add_node("^")
        o1 = graph.add_node("^")
        o2 = graph.add_node("^")

        graph.add_edge(i0, o0)
        graph.add_edge(i0, o1)
        graph.add_edge(i1, o0)
        graph.add_edge(i1, o2)
        graph.add_edge(i2, o1)
        graph.add_edge(i2, o2)
        graph.add_edge(i3, o0)
        graph.add_edge(i3, o1)
        graph.add_edge(i3, o2)

        return graph

    @classmethod
    def decoder(cls):
        graph = bool_circ.empty()
        n0 = graph.add_node()
        n1 = graph.add_node()
        n2 = graph.add_node()
        i0 = graph.add_node()
        i1 = graph.add_node()
        i2 = graph.add_node()
        i3 = graph.add_node()
        o0 = graph.add_node("^")
        o1 = graph.add_node("^")
        o2 = graph.add_node("^")
        graph.add_edge(i0, o0)
        graph.add_edge(i0, o1)
        graph.add_edge(i1, o0)
        graph.add_edge(i1, o2)
        graph.add_edge(i2, o1)
        graph.add_edge(i2, o2)
        graph.add_edge(i3, o0)
        graph.add_edge(i3, o1)
        graph.add_edge(i3, o2)
        graph.add_edge(n0, o0)
        graph.add_edge(n1, o1)
        graph.add_edge(n2, o2)
        m0 = graph.add_node()
        m1 = graph.add_node()
        m2 = graph.add_node()
        graph.add_edge(o0, m0)
        graph.add_edge(o1, m1)
        graph.add_edge(o2, m2)
        and_0 = graph.add_node("&")
        and_1 = graph.add_node("&")
        and_2 = graph.add_node("&")
        and_3 = graph.add_node("&")
        not_0 = graph.add_node("~")
        not_1 = graph.add_node("~")
        not_2 = graph.add_node("~")
        graph.add_edge(m0, and_0)
        graph.add_edge(m0, and_1)
        graph.add_edge(m0, not_2)
        graph.add_edge(m0, and_2)
        graph.add_edge(m1, and_0)
        graph.add_edge(m1, not_1)
        graph.add_edge(m1, and_2)
        graph.add_edge(m1, and_3)
        graph.add_edge(m2, not_0)
        graph.add_edge(m2, and_1)
        graph.add_edge(m2, and_2)
        graph.add_edge(m2, and_3)
        o0_1 = graph.add_node("^")
        o1_1 = graph.add_node("^")
        o2_1 = graph.add_node("^")
        graph.add_edge(o0_1, i0)
        graph.add_edge(o1_1, i1)
        graph.add_edge(o2_1, i2)
        return graph

    def trans_asso_xor(self, nid):
        n = self.get_node_by_id(nid)

        if n.get_label() == "^":
            for cid in n.get_children_ids():
                child = self.get_node_by_id(cid)
                
                if child.get_label() == "^":                
                    for id in n.get_children_ids():
                        child.add_parent_id(id)
                
                    child.remove_parent_id(nid)
                    self.remove_node_by_id(nid)
    
    def trans_asso_copie(self, nid):
        n = self.get_node_by_id(nid)
        
        if n.get_label() == "":
            for cid in n.get_children_ids():
                child = self.get_node_by_id(cid)

                if child.get_label() == "":
                    for id in child.get_children_ids():
                        self.add_edge(nid, id)

                    n.remove_child_id(cid)
                    self.remove_node_by_id(cid)

    def trans_invo_xor(self, nid):
        n = self.get_node_by_id(nid)
    
        if n.get_label() == "^":
            if len(n.get_children_ids()) %2 == 0:
                 self.remove_nodes_by_id(n.get_children_ids())
            
            else:
                self.remove_nodes_by_id(n.get_children_ids()[1:])

    def trans_effacement(self, nid):
        OP = ["^", "&", "~", ""]
        n = self.get_node_by_id(nid)
        
        if n.get_label() in OP:
            for pid in n.get_parents_ids():
                copie = self.add_nodes()
                self.add_edge(copie, pid)

            for cid in n.get_parents_ids():
                copie = self.add_nodes()
                self.add_edge(copie, cid)

            self.remove_node_by_id(nid)

    def trans_invo_no(self, nid):
        n = self.get_node_by_id(nid)
        has_removed = False

        if n.get_label() == "~":
            for cid in n.get_children_ids():
                child = self.get_node_by_id(cid)
        
                if child.get_label() == "~":
                    for pid in n.get_children_ids():
                        self.add_edge(pid, cid)

                    self.remove_node_by_id(cid)
            
            if has_removed:
                self.remove_node_by_id(nid)

    def trans_no_travers_xor(self, nid):
        n = self.get_node_by_id(nid)
        
        if n.get_label() == "^":
            pass
            # for 