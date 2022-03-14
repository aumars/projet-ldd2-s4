from urllib.parse import quote
import re
import os


class op_display_mx:
    def __str__(self):
        if len(self.get_id_node_map()) == 0:
            return 'empty'
        else:
            return "{{ {}, I = {{ {} }}, O = {{ {} }}, {} }}".format(", ".join([str(node) for node in self.nodes.values()]),
                                                                  ", ".join([str(id) for id in self.get_input_ids()]),
                                                                  ", ".join([str(id) for id in self.get_output_ids()]),
                                                                  ", ".join([str(node) + " -> " + str(self.get_node_by_id(child))
                                                                             for node in self.nodes.values()
                                                                             for child in node.children.keys()]))

    def __repr__(self):
        return str(self)

    def to_str_dot_format(self, verbose=False):
        """
        Generate a string of the dot format.
        
        Parameters
        ----------
        verbose : boolean, optional
            Set to True to display the nodes IDs. 

        Returns
        ------
        string
           The string of the graph in dot format.
        """
        digraph = "digraph G {\n"

        for node in self.get_nodes():
            form = ("shape=invhouse, " if node.get_id() in self.get_input_ids() else 
                       "shape=house, " if node.get_id() in self.get_output_ids() else "")
            
            id_str = f"\nid: {node.get_id()}" if verbose else ""

            digraph += f"v{ node.get_id() } [{form}label=\"{ node.get_label() }{ repr(id_str)[1:-1] }\"];\n"
        
        for node in self.get_nodes():  
            for parent in node.get_parent_ids():
                line = f"v{parent} -> v{node.get_id()};\n"
                digraph += line * node.get_parent_multiplicity(parent)
        
        digraph += "}"

        return digraph
    
    def save_as_dot_file(self, path, verbose=False):
        """
        Save the graph as dot file.
        
        Parameters
        ----------
        path:
            The path where the file will be saved. Must be in '.dot' format.

        verbose : boolean, optional
            Set to True to display the nodes IDs. 
        """
        f = open(path, "w")
        f.write(self.to_str_dot_format(verbose))
        f.close()

    @classmethod
    def from_dot_file(self, path):
        """
        Create a graph from dot file.
        
        Parameters
        ----------
        path:
            The path where the dot file is saved.

        Returns
        ------
        open_digraph
           The graph corresponds to the file.        
        """
        with open(path, "r") as file:
            f = file.read()
        f = f.split("{")[1].split("}")[0].replace(" ", "").replace("\n", "").split(";")
        f = [l for l in f if l != ""]

        graph = self.empty()
        dict_node = {}

        in_dict = lambda label: set(dict_node.keys()) & set(label) != set()
        add_node = lambda label: {"id": graph.add_node(label), "parents":set(), "children": set()}
        get_id_dict = lambda label : add_node(label) if not in_dict(label) else dict_node[str_node]["id"]

        for line in f:
            lbl_re = re.search(r".*label=\"(.*?)\"\]", line)
            lbl_node = lbl_re.group(1) if lbl_re != None else ""

            line = line.strip().split("[")[0]

            n_node = len(line.split("->"))
            l = line.split("->")

            for i in range(n_node):
                str_node = line.split("->")[i]                
                dict_node[str_node] = get_id_dict(lbl_node)

                if not lbl_node in dict_node:
                    add_node(lbl_node)
                
                else:
                    l_parents = [get_id_dict(parent) for parent in l[:i]]
                    l_children = [get_id_dict(child) for child in l[i+1:]]

                    dict_node[str_node]["parents"] = dict_node[str_node]["parents"].union(l_parents)
                    dict_node[str_node]["children"] = dict_node[str_node]["children"].union(l_children)

        for str_node in dict_node:
            graph.get_node_by_id(dict_node[str_node]["id"]).set_parent_ids(dict_node[str_node]["parents"])
            graph.get_node_by_id(dict_node[str_node]["id"]).set_children_ids(dict_node[str_node]["children"])
        
        return graph

    def display(self, verbose=False):
        """
        Display the graph in the following website : dreampuf.github.io/GraphvizOnline.
        
        Parameters
        ----------
        verbose : boolean, optional
            Set to True to display the nodes IDs. 
        """
        digraph = quote(self.to_str_dot_format(verbose))
        url = f'https://dreampuf.github.io/GraphvizOnline/#"{digraph}"'
        os.system(f"firefox {url}")