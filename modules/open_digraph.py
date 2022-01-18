class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
        
    def __str__(self):
        return "N({})".format(self.id)

    def __repr__(self):
        return str(self)

    def copy(self):
        return node(self.id, self.label, self.parents, self.children)

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parents_ids(self):
        return self.parents.keys()

    def get_children_ids(self):
        return self.chlidren.keys()

    def set_id(self, id):
        self.id = id

    def set_label(self, label):
        self.label = label

    def set_parents_ids(self, parents_ids):
        self.parents = parents_ids

    def set_children_ids(self, children_ids):
        self.children = children_ids

    def add_child_id(self, child):
        if child not in self.children.keys():
            self.children[child] = 1
        else:
            self.children[child] += 1

    def add_parent_id(self, parent):
        if parent not in self.parents.keys():
            self.children[parent] = 1
        else:
            self.children[parent] += 1

class open_digraph: # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

    def __str__(self):
        return """Noeuds : {}
Arrêts : {}""".format([str(node) for node in self.nodes.values()],
                      [str(node) + " -> " + str(child) for node in self.nodes.values() for child in node.children.keys()])

    def __repr__(self):
        return str(self)

    @classmethod
    def empty(self):
        self.inputs = []
        self.outputs = []
        self.nodes = {}

    def copy(self):
        return open_digraph(self.inputs, self.outputs, self.nodes.values())

    def get_intputs_ids(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def get_id_node_map(self):
        return self.nodes

    def get_nodes(self):
        return self.nodes.values

    def get_nodes_ids(self):
        return self.nodes.keys()

    def get_node_by_id(self, id):
        return self.nodes[id]

    def get_nodes_by_ids(self, ids):
        return [self.get_node_by_id(id) for id in ids]


    def set_input_ids(self, inputs):
        self.inputs = inputs

    def set_output_ids(self, outputs):
        self.outputs = outputs

    def add_input_id(self, id):
        if id not in self.inputs:
            self.inputs.append(id)

    def add_output_id(self, id):
        if id not in self.outputs:
            self.outputs.append(id)

    def new_id(self):
        # MAXINT erreur
        # O(n)
        return max(self.nodes.keys()) + 1

    def add_edge(self, src, tgt):
        self.nodes[src].add_child(tgt)
        self.nodes[tgt].add_parent(src)

    def add_node(self, label='', parents=[], children=[]):
        n0 = node(self.new_id(), label, parents, children)
        self.nodes[n0.get_id()] = n0
        for parent in parents:
            self.nodes[parent].add_child_id(n0.get_id())
        for child in children:
            self.nodes[child].add_parent_id(n0.get_id())
