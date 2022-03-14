from random import random, sample
from modules.utils import (random_int_matrix,
                           random_triangular_int_matrix,
                           random_oriented_int_matrix,
                           random_symetric_int_matrix)


class op_special_graph_mx:
    @classmethod
    def empty(self):
        """Create an empty graph."""
        return self([], [], {})

    @classmethod
    def identity(cls, n):
        """
        The identity graph.

        Parameters
        ----------
        n : int
           The number of input and output.

        Returns
        ------
        open_digraph
           The identity graph composed of n inputs and n outputs.
        """
        graph = cls.empty()

        for _ in range(2 * n):
            graph.add_node()

        for i in range(2 * n):
            if i % 2 == 0:
                graph.add_edge(i, i + 1)

        graph.set_input_ids([2 * i for i in range(n + 1)])
        graph.set_output_ids([2 * i + 1 for i in range(n + 1)])

        return graph

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free",
               number_generator=random):
        """
        Generate random graph.

        Parameters
        ----------
        n : int
            Length of list
        bound : int
            Upper bound of our random positive integers.
        inputs : int, optional
            Number of input nodes.
        outputs : int, optional
            Number of output nodes.
        form : str, optional
            Type of graph, here are the available options:
            - free : Completely random graph.
            - loop-free : Random graph with no edge between the same node.
            - undirected : Undirected graph
            - loop-free undirected : Undirected graph with no edge between the
                                     same node.
            - oriented : Directed graph with the edges of each pair of nodes
                         pointing only towards one end.
            - DAG : Directed acyclic graph.
        number_generator : callable, optional
            Random number generator that generates real numbers between 0 and 1
            (included or excluded). If [number_generator] generates real
            positive numbers, only the non-integer part is kept.

        Returns
        -------
        open_digraph
           Graph

        Raises
        ------
        ValueError
            If [value] is not recognised as a supported option.
        """
        if inputs > n or outputs > n:
            raise ValueError("More inputs and outputs than available.")
        input_children = sample(range(n), k=inputs)
        output_parents = sample(range(n), k=outputs)
        if form == "free" or form == "loop-free":
            if form == "free":
                A = random_int_matrix(n, bound, null_diag=False,
                                      number_generator=number_generator)
            else:
                A = random_int_matrix(n, bound,
                                      number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        elif form == "undirected" or form == "loop-free undirected":
            if form == "undirected":
                A = random_symetric_int_matrix(n, bound, null_diag=False,
                                               number_generator=number_generator)
            else:
                A = random_symetric_int_matrix(n, bound,
                                               number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
                    A[i][j] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
                    A[j][i] = 0
        elif form == "oriented":
            A = random_oriented_int_matrix(n, bound,
                                           number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        elif form == "DAG":
            A = random_triangular_int_matrix(n, bound,
                                             number_generator=number_generator)
            for i in input_children:
                for j in range(n):
                    A[j][i] = 0
            for i in output_parents:
                for j in range(n):
                    A[i][j] = 0
        else:
            return ValueError("{} is not a supported option."
                              .format(form))
        G = cls.graph_from_adjacency_matrix(A)
        for i in input_children:
            G.add_input_node(i)
        for o in output_parents:
            G.add_output_node(o)
        return G
