class op_matrix_mx:
    @classmethod
    def graph_from_adjacency_matrix(cls, A):
        """
        Generate graph from adjacency matrix.

        Parameters
        ----------
        A : list list int
            Adjacency matrix

        Returns
        -------
        open_digraph
           Graph
        """
        G = cls.empty()
        n = len(A)
        node_ids = [G.add_node() for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(A[i][j]):
                    G.add_edge(node_ids[i], node_ids[j])
        return G
        
    def adjacency_matrix(self):
        """
        Generate the adjacency matrix of a graph.

        Returns
        ------
        list list int
           Adjacency matrix
        """
        dict = self.node_dict()
        n = len(dict)
        A = [[0 for _ in range(n)] for _ in range(n)]
        for id in dict:
            i = dict[id]
            node = self.get_node_by_id(id)
            for child in node.get_children_ids():
                j = dict[child]
                A[i][j] = node.get_child_multiplicity(child)
        return A