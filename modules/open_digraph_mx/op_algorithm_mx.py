from operator import itemgetter


class op_algorithm_mx:
    def dijkstra(self, src, tgt=None, direction=None):
        """
        The Dijkstra Algorithm.
        Get the path connecting a source and a target node.

        Parameters
        ----------
        src : int
            The ID of the source node.
        tgt : int, optional
            The ID of the target node. If it's None return the shrotest path. Value by default.
        direction : int, optional
            The direction of the algorithm's path. There is three possibilty : 
            -1 : Search only in direction for parents. 
            1 : Search only in direction for children. 
            None : Search in direction for children and parents. Value by default.

        Returns
        -------
        int -> node dict
            The distance of each node in the path of the scr node, according to the direction.
        int -> node dict
            A dictionnary of the path. Keys are node in the path. And values are the ancestor of the key node.
        Raises
        ------
        ValueError
            If [src] or [tgt] (except None) is not a valid node ID
        """
        if src not in self.get_node_ids() or (not (tgt is None) and tgt not in self.get_node_ids()):
            raise ValueError(f"src = {src} must be a valid node and tgt = {tgt} must either be a valid node or None")
        Q = [src]
        dist = {src: 0}
        prev = {}

        while Q != []:
            u = min(dist, key=dist.get)
            Q.remove(u)

            neighbours = []

            if direction == 1 or direction == None:
                neighbours = self.get_node_by_id(u).get_children_ids()

            if direction == -1 or direction == None:
                neighbours += self.get_node_by_id(u).get_parent_ids()

            for v in neighbours:
                if v not in dist.keys():
                    neighbours.append(v)

                if v not in dist.keys() or dist[v] > dist[u] + 1:
                    dist[v] = dist[u] + 1
                    prev[v] = u

            if u == tgt:
                return dist, prev

        return dist, prev

    def shortest_path(self, src, tgt):
        """
        Compute the shortest path connecting source and target node.

        Parameters
        ----------
        src : int
            The ID of the source node.
        tgt : int
            The ID of the target node. If it's None return the shrotest path.

        Returns
        -------
        int list
            The shortest path connecting source and target node.
        """
        __, prev = self.dijkstra(src, tgt, direction=1)
        parent = tgt
        path = [tgt]
        while parent != src:
            path.insert(0, prev[parent])
            parent = prev[parent]

        return path

    def common_ancestry(self, n0, n1):
        """
        Compute common ancestry between two nodes. 

        Parameters
        ----------
        n0 : int
            The ID of the first node.
        n1 : int
            The ID of the second node.

        Returns
        -------
        int -> int * int
            Keys representing common ancestry. And values are the respectives distances.
        """
        dist_0, prev_O = self.dijkstra(n0, direction=-1)
        dist_1, prev_1 = self.dijkstra(n1, direction=-1)

        common = set(prev_O.keys()).intersection(set(prev_1))
        result = {}

        for n in common:
            result[n] = (dist_0[n], dist_1[n])

        return result

    def topological_sort(self):
        """
        Compute the topological sorted.

        Returns
        -------
        int list list
            The list of int list of the topological sorted.
        
        Raises
        ------
        ValueError
            If the boolean circuit is cyclic.
        """
        if self.is_cyclic():
            raise ValueError("The graph can't be cyclic.")

        result = [[]]
        etage = 1

        I = set(self.get_input_ids())
        NON_INPUTS = set(self.get_nodes()) - I

        for i in I:
            result[0] += self.get_node_by_id(i).get_children_ids()

        for node in NON_INPUTS:
            if node.get_parent_ids() == []:
                result[0].append(node.get_id())

        while True:
            result.insert(etage, [])

            children = set()

            for n_id in result[etage-1]:
                node = self.get_node_by_id(n_id)
                children = set(node.get_children_ids())

                for child in children:
                    if not child in result[etage]:
                        result[etage].append(child)

            if children == set():
                break

            else:
                etage += 1

        seen = []
        for i in range(len(result)-1, 0, -1):
            for j in result[i]:
                if j in seen:
                    result[i] = list(filter(lambda x: x != j, result[i]))

                else:
                    seen += [j]

        return result

    def node_depth(self, node):
        """
        Get the depth a node in the graph.

        Parameters
        ----------
        node : int
            The ID of the node.

        Returns
        -------
        int
            The node depth.
        
        Raises
        ------
        ValueError
            If the boolean circuit is cyclic.
        """
        if self.is_cyclic():
            raise ValueError("The graph can't be cyclic.")
        
        topo_sort = self.topological_sort()

        for i in range(len(topo_sort)):
            if node in topo_sort[i]:
                return i

    def depth(self):
        """
        Get the graph depth.

        Returns
        -------
        int
            The graph depth.
        """
        return len(self.topological_sort())

    def longest_path(self, src, tgt):
        """
        Get the longest path in the graph.

        Parameters
        ----------
        src : int
            The ID of the source node.
        tgt : int
            The ID of the target node.

        Returns
        -------
        int list
            The longest path.
        int
            The distance of the longest path.
        """
        if self.is_cyclic():
            raise ValueError("The graph can't be cyclic.")

        topological_sort = self.topological_sort()

        dist, prev = {}, {}
        id_lk = 0

        for i in range(len(topological_sort)):
            if src in topological_sort[i]:
                id_lk = i

        for next_l in topological_sort[id_lk+1:]:
            for w in next_l:
                if w != tgt:
                    w_parents = self.get_node_by_id(w).get_parent_ids()
                    depth_list = [(self.node_depth(p), p) for p in w_parents]
                    max_w_parents = max( depth_list, key=itemgetter(0) )

                    for parent in w_parents:
                        if parent in dist[w]:
                            dist[w] = max_w_parents[0] + 1
                            prev[w] = max_w_parents[1]
                            break
        
        return dist.keys(), len(dist.keys())
                            