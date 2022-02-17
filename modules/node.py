class node:
    def __init__(self, identity, label, parents, children):
        """
        A graph node.

        Parameters
        ----------
        identity : int
            Its unique ID in the graph.
        label : str
            A string.
        parents : int->int dict
            Maps a parent node's id to its multiplicity. All values must be
            positive integers. Zero values are ignored.
        children : int->int dict
            Maps a child node's id to its multiplicity. All values must be
            positive integers. Zero values are ignored.

        Raises
        ------
        ValueError
            If a value in [parents] or [children] is strictly negative.
        """
        for key, value in parents.items():
            if value < 0:
                raise ValueError("ID {} must be positive: {}"
                                 .format(key, value))
        for key, value in children.items():
            if value < 0:
                raise ValueError("ID {} must be positive: {}"
                                 .format(key, value))

        self.id = identity
        self.label = label
        self.parents = {k: v for k, v in parents.items() if v >= 1}
        self.children = {k: v for k, v in children.items() if v >= 1}

    def __str__(self):
        return "N({})".format(self.id)

    def __repr__(self):
        return str(self)

    def copy(self):
        """
        Copy the node.

        Returns
        -------
        node
            The copy of this node.
        """
        return node(self.id, self.label, self.parents, self.children)

    def get_id(self):
        """
        Get the ID.

        Returns
        -------
        int
            The node ID.
        """
        return self.id

    def get_label(self):
        """
        Get the label.

        Returns
        -------
        string
            The node label.
        """
        return self.label

    def get_parent_ids(self):
        """
        Get the IDs of all the parents.

        Returns
        -------
        int list
            A list containing the IDs of all parents.
        """
        return list(self.parents.keys())

    def get_children_ids(self):
        """
        Get the IDs of all the children.

        Returns
        -------
        int list
            A list containing the IDs of all children.
        """
        return list(self.children.keys())

    def get_parent_multiplicity(self, id):
        """
        Get the multiplicity of a parent

        Parameters
        ----------
        id : int
            The ID of the parent node.

        Returns
        -------
        int
            The multiplicity of the parent node.
        """
        return self.parents.get(id, 0)

    def get_child_multiplicity(self, id):
        """
        Get the multiplicity of a child

        Parameters
        ----------
        id : int
            The ID of the child node.

        Returns
        -------
        int
            The multiplicity of the child node.
        """
        return self.children.get(id, 0)

    def set_id(self, id):
        """
        Set the node ID.

        Parameters
        ----------
        id : int
            The node ID.
        """
        self.id = id

    def set_label(self, label):
        """
        Set the node label.

        Parameters
        ----------
        label : str
            The node label.
        """
        self.label = label

    def set_parent_ids(self, parents_ids):
        """
        Set the parents of the node.

        Parameters
        ----------
        parents_ids : int list
            A list containing the IDs of the parent nodes. The number of
            occurrences of each unique ID is the multiplicity of the parent
            node.
        """
        self.parents.clear()
        for id in parents_ids:
            self.parents[id] = self.parents.get(id, 0) + 1

    def set_children_ids(self, children_ids):
        """
        Set the children of the node.

        Parameters
        ----------
        children_ids : int list
            A list containing the IDs of the child nodes. The number of
            occurrences of each unique ID is the multiplicity of the child
            node.
        """
        self.children.clear()
        for id in children_ids:
            self.children[id] = self.children.get(id, 0) + 1

    def add_parent_id(self, parent):
        """
        Add a new parent to the node.

        Parameters
        ----------
        parent : int
            The ID of the parent node.
        """
        self.parents[parent] = self.parents.get(parent, 0) + 1

    def add_child_id(self, child):
        """
        Add a new child to the node.

        Parameters
        ----------
        child : int
            The ID of the child node.
        """
        self.children[child] = self.children.get(child, 0) + 1

    def remove_parent_once(self, id):
        """
        Remove one occurence of a parent node.
        
        If the given parent ID does not exist, nothing happens.

        Parameters
        ----------
        id : int
            The ID of the parent node.
        """
        if id in self.get_parent_ids():
            if self.parents[id] == 1:
                del self.parents[id]
            else:
                self.parents[id] -= 1

    def remove_child_once(self, id):
        """
        Remove one occurence of a child node.
        
        If the given child ID does not exist, nothing happens.

        Parameters
        ----------
        id : int
            The ID of the child node.
        """
        if id in self.get_children_ids():
            if self.children[id] == 1:
                del self.children[id]
            else:
                self.children[id] -= 1

    def remove_parent_id(self, id):
        """
        Remove all occurences of a parent node.
        
        If the given parent ID does not exist, nothing happens.

        Parameters
        ----------
        id : int
            The ID of the parent node.
        """
        if id in self.get_parent_ids():
            del self.parents[id]

    def remove_child_id(self, id):
        """
        Remove all occurences of a child node.
        
        If the given parent ID does not exist, nothing happens.

        Parameters
        ----------
        id : int
            The ID of the child node.
        """
        if id in self.get_children_ids():
            del self.children[id]

    def indegree(self):
        """
        Get the degree of input.

        Returns
        -------
        int
            The degree of input.
        """
        return sum(self.parents.values())
    
    def outdegree(self):
        """
        Get the degree of output.

        Returns
        -------
        int
            The degree of output.
        """
        return sum(self.children.values())
    
    def degree(self):
        """
        Get the total degree.

        Returns
        -------
        int
            The total degree.
        """
        return self.outdegree() + self.indegree()