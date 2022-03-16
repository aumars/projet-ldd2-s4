class op_algorithm_mx:
    def dijkstra(self, src, tgt=None, direction=None):
        Q = [src]
        dist = {src:0}
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
        __, prev = self.dijkstra(src, tgt, direction=1)
        parent = tgt
        path = [tgt]
        while (parent != src):
            path.insert(0, prev[parent])
            parent = prev[parent]

        return path

    def common_ancestry(self, n0, n1):
        dist_0, prev_O = self.dijkstra(n0, direction=-1)
        dist_1, prev_1 = self.dijkstra(n1, direction=-1)

        common = set(prev_O.keys()).intersection(set(prev_1))
        result = {}

        for n in common:
            result[n] = (dist_0[n], dist_1[n])

        return result


    def topological_sort(self):
        if self.is_cyclic(): 
            raise ValueError("The graph can't be cyclic.")
        
        result = [[]]
        etage = 1
        
        I = set(self.get_input_ids())
        NON_INPUTS = set(self.get_nodes()) - I

        # On ajoute les enfants d'inputs
        for i in I:
            result[0] += self.get_node_by_id(i).get_children_ids()

        # On rajoute les noeuds sans enfants
        for node in NON_INPUTS:
            if node.get_parent_ids() == []:
                result[0].append(node.get_id())

        # On créer un nouveau etage
        while True:
            result.insert(etage, [])

            for n_id in result[etage-1]:
                node = self.get_node_by_id(n_id)
                CHILDREN = set(node.get_children_ids())

                for child in CHILDREN:
                    if not child in result[etage]:
                        result[etage].append(child)
                    

            if CHILDREN == set(): 
                break
            
            else:
                etage += 1
        
        # Remove duplicate
        seen = []
        for i in range(len(result)-1, 0, -1):
            for j in result[i]:
                if j in seen:
                    result[i] = list(filter(lambda x: x!=j, result[i]))

                else:
                    seen += [j]


        return result

    def depth_node(self, node):
        topo_sort = self.topological_sort()
        
        for i in range(len(topo_sort)):
            if node in topo_sort[i]:
                return i

