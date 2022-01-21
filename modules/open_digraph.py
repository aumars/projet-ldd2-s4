class node:
    def __init__(self, identity, label, parents, children):
        """
        A node.

        Args:
            identity (int): Its unique ID in the graph.
            label (string): A string.
            parents (int->int dict): Maps a parent node's id to its multiplicity
            children (int->int dict): Maps a child node's id to its multiplicity
        """
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self):
        return "N({})".format(self.id)

    def __repr__(self):
        return str(self)

    def copy(self):
        """
        Copy the node.

        Returns:
            node: The copy of this node.
        """
        return node(self.id, self.label, self.parents, self.children)

    def get_id(self):
        """
        Get the ID.

        Returns:
            int: The node ID.
        """
        return self.id

    def get_label(self):
        """
        Get the label.

        Returns:
            string: The node label.
        """
        return self.label

    def get_parent_ids(self):
        """
        Get the IDs of all the parents.

        Returns:
            list: A list containing the ids of all parents.
        """
        return list(self.parents.keys())

    def get_children_ids(self):
        """
        Get the IDs of all the children.

        Returns:
            list: A list containing the ids of all children.
        """
        return list(self.children.keys())

    def set_id(self, id):
        """
        Set the node ID.

        Args:
            id (int): The node ID.
        """
        self.id = id

    def set_label(self, label):
        """
        Set the node label.

        Args:
            label (string): The node label.
        """
        self.label = label

    def set_parent_ids(self, parents_ids):
        """
        Set the parents of the node.

        Args:
            parents_ids (int->int dict): A dictionary containing the parents of the node.
        """
        self.parents.clear()
        for parent in parents_ids:
            self.parents[parent] = 1

    def set_children_ids(self, children_ids):
        """
        Set the children of the node.

        Args:
            children_ids (int->int dict): A dictionary containing the children of the node.
        """
        self.children.clear()
        for child in children_ids:
            self.children[child] = 1

    def add_child_id(self, child):
        """
        Add a new child to the node.

        Args:
            child (int): The ID of the child node.
        """
        if child not in self.children.keys():
            self.children[child] = 1
        else:
            self.children[child] += 1

    def add_parent_id(self, parent):
        """
        Add a new parent to the node.

        Args:
            parent (int): The ID of the parent node.
        """
        if parent not in self.parents.keys():
            self.parents[parent] = 1
        else:
            self.parents[parent] += 1


class open_digraph:  # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        """
        A graph composed of nodes.
        Args:
            inputs (int list): The IDs of the input nodes.
            outputs (int list): The IDs of the output nodes.
            nodes (iter): Node iter.
        """
        self.inputs = inputs
        self.outputs = outputs
        # self.nodes: <int,node> dict
        self.nodes = {node.id: node for node in nodes}
        self.next_id = max(self.nodes.keys()) + 1

    def __str__(self):
        return """Noeuds : {}
Arrêts : {}""".format([str(node) for node in self.nodes.values()],
                      [str(node) + " -> " + str(child)
                       for node in self.nodes.values()
                       for child in node.children.keys()])

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(self):
        """Create an empty graph."""
        self.inputs = []
        self.outputs = []
        self.nodes = {}
        self.next_id = 0

    def copy(self):
        """
        Copy this graph.

        Returns:
            open_digraph: The copy of this graph.
        """
        return open_digraph(self.inputs, self.outputs, self.nodes.values())

    def get_input_ids(self):
        """
        Get the inputs IDs.

        Returns:
            int list: The list of the inputs IDs
        """
        return self.inputs

    def get_output_ids(self):
        """
        Get the outputs IDs.

        Returns:
            int list: The list of the outputs IDs
        """
        return self.outputs

    def get_id_node_map(self):
        """
        Get all nodes.

        Returns:
            <int, node> dict: A dictionary containing nodes.
        """
        return self.nodes

    def get_nodes(self):
        """
        Get all nodes.

        Returns:
            int list: A list containing nodes.
        """
        return list(self.nodes.values())

    def get_node_ids(self):
        """
        Get all IDs of nodes.

        Returns:
            int list: A list containing the IDs of the nodes.
        """
        return list(self.nodes.keys())

    def get_node_by_id(self, id):
        """
        Get the node with an ID.

        Args:
            id (int): The id of the node.

        Returns:
            node: The node with this id.
        """
        if id in self.nodes.keys():
            return self.nodes[id]
        else:
            raise KeyError("id {} n'existe pas !".format(id))

    def get_nodes_by_ids(self, ids):
        """
        Get nodes corresponding to the IDs passed in parameter.

        Args:
            ids (int list): The list of node IDs to return.

        Returns:
            node list: A list containing nodes corresponding to the IDs.
        """
        return [self.get_node_by_id(id) for id in ids]

    def set_input_ids(self, inputs):
        """
        Set the inputs IDs.

        Args:
            inputs (int list): The input list.
        """
        self.inputs = inputs

    def set_output_ids(self, outputs):
        """
        Set the outputs IDs.

        Args:
            outputs (int list): The outputs list.
        """
        self.outputs = outputs

    def add_input_id(self, id):
        """
        Add a new input ID.

        Args:
            id (int): The input ID to add.
        """
        if id not in self.inputs:
            self.inputs.append(id)

    def add_output_id(self, id):
        """
        Add a new output ID.

        Args:
            id (int): The output ID to add.
        """
        if id not in self.outputs:
            self.outputs.append(id)

    def new_id(self):
        """
        Generate a new ID.

        Returns:
            int: A new ID.
        """
        # https://stackoverflow.com/a/982100
        self.next_id += 1
        return self.next_id - 1

    def add_edge(self, src, tgt):
        """
        Add a new edge from 'src' node to 'tgt' node.
        Args:
            src (int): The ID of the source node.
            tgt (int): The ID of the target node.
        """
        if src in self.get_output_ids():
            raise ValueError("Noeud {} est un noeud sortant ! On peut pas "
                             "ajouter une flèche à partir de ce "
                             "noeud.".format(src))
        if tgt in self.get_input_ids():
            raise ValueError("Noeud {} est un noeud entrant ! On peut pas "
                             "ajouter une flèche vers ce noeud.".format(src))
        self.nodes[src].add_child_id(tgt)  # replace add_child with add_child_id ?
        self.nodes[tgt].add_parent_id(src)  # replace add_parent with add_parent_id ?

    def add_node(self, label='', parents=[], children=[]):
        """
        Add a new node in the graph. Then links it with parent and child nodes.

        Args:
            label (str, optional): The label of the new node. Defaults to ''.
            parents (list, optional): The parents list of the new node. Defaults to [].
            children (list, optional): The children list of the new node. Defaults to [].
        """
        O = set(parents) & set(self.get_output_ids())
        if O != set():
            raise ValueError("Les noeuds suivants sont des noeuds sortants et "
                             "ne peuvent pas être parents : {}".format(O))
        I = set(children) & set(self.get_input_ids())
        if I != set():
            raise ValueError("Les noeuds suivants sont des noeuds entrants et "
                             "ne peuvent pas être enfants : {}".format(I))
        n0 = node(self.new_id(), label, parents, children)
        self.nodes[n0.get_id()] = n0
        for parent in parents:
            self.nodes[parent].add_child_id(n0.get_id())
        for child in children:
            self.nodes[child].add_parent_id(n0.get_id())
