class op_tools_mx:
    def reverse_dict(self, dict):
        """
        Reverse the dict.
        The values of dict become keys. The keys are regrouped in a list and associated to values.

        Parameters
        ----------
        dict : int -> int
           The dict to inverted.
        
        Returns
        ------
        int -> list
           The dictionary reversed.
        """ 
        invert = {}

        for key, val in dict.items():
            invert[val] = [key] if val not in invert.keys() else invert[val] + [key]
        
        return invert