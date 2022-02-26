class op_setter_mx:
    def set_input_ids(self, inputs):
        """
        Set the inputs IDs.

        Parameters
        ----------
        inputs : int list
            The input list. Duplicates are removed.
        """
        self.inputs = list(dict.fromkeys(inputs))

    def set_output_ids(self, outputs):
        """
        Set the outputs IDs.

        Parameters
        ----------
            The input list. Duplicates are removed.
        """
        self.outputs = list(dict.fromkeys(outputs))

    def set_nodes(self, nodes):
        self.nodes = {node.get_id(): node for node in nodes}
