class op_connected_components_mx:
    def get_heritage(self, id, result, nodes_seen=[], to_parents=True):
        """
        Get the IDs list of all nodes having a possible path with the node 'id'
        in the graph.

        Parameters
        ----------
        id : int
           The ID of the node we want to have the heritage.

        result: int list
            The list where IDs are stored.

        node_seen: int_list, optional
            The list containing the nodes seen. This argument is to optimize the graph path.
            During the traversal of the graph, if a node has already been seen, then the 
            traversal is stopped.
        
        to_parents: boolean, optional
            Determines the traversal direction of the graph. By default, is True, then the direction is 
            node to his parents. If False, it's the opposite direction node to his children.
        """ 
        result.add(id)
        node = self.get_node_by_id(id)

        in_out_nodes = self.get_input_ids() if to_parents else self.get_output_ids()

        if id in nodes_seen or id in in_out_nodes:
            return result
        
        else:
            child_parent_nodes = node.get_parent_ids() if to_parents else node.get_children_ids()
            
            for child_parent in child_parent_nodes:
                self.get_heritage(child_parent, result, nodes_seen=nodes_seen)
   
    def assoc_nodes_to_comp(self, nodes, dict_comp):
        """
        Associated each node of a list with its components.

        Parameters
        ----------
        nodes : int list
           The IDs of nodes to associate.

        dict_comp: int -> int
            The dict where the assocation are stored. The keys corresponds to node ID. 
            And values corresponds the ID of the component where the node is connected.

        """ 
        for n_id in nodes:
            component = set([n_id])

            for child in self.get_node_by_id(n_id).get_parent_ids():
                self.get_heritage(child, component, nodes_seen=dict_comp.keys()) 
                
                I = set(dict_comp.keys()).intersection(component)
                group_comp = len(set(dict_comp.values())) if I == set() else dict_comp[list(I)[0]]
                
                dict_comp.update({id: group_comp for id in component})

    def connected_components(self):
        """
        Get the dict which associte each node with its connected components.
       
        Returns
        ------
        int * (int -> list)
           The number of connected components and a dict where each node are associated
           with its component.
        """ 
        dict_comp = {}

        self.assoc_nodes_to_comp(self.get_output_ids(), dict_comp)
        self.assoc_nodes_to_comp(set(self.get_node_ids()) - set(dict_comp.keys()), dict_comp)

        return len(set(dict_comp.values())), dict_comp

    def get_connected_components(self):
        """
        Separated the connected components of the graphs.

        Returns
        ------
        open_digraph list
           A list containing the separated graphs.
        """ 
        n_comp, connected_comp = self.connected_components()
        connected_comp = self.reverse_dict(connected_comp)
        list_comps = []

        for i in range(n_comp):
            nodes_ids = connected_comp[i]
            
            nodes = self.get_nodes_by_ids(nodes_ids)
            inputs = set(self.get_input_ids()).intersection(nodes_ids)
            outputs = set(self.get_output_ids()).intersection(nodes_ids)
            
            graph = super().__init__(list(inputs), list(outputs), nodes)
            self.open_digraph()
            
            list_comps.append(graph)

        return list_comps
 